from charm.core.math.elliptic_curve import ZR
from django import forms
from django.contrib import messages
from django.db.models import F
from django.shortcuts import render, redirect
from app01 import models
from app01.utils import Pulp
from charm.toolbox.eccurve import prime192v2
from charm.toolbox.ecgroup import ECGroup

group = ECGroup(prime192v2)


class TrapdoorModelForm(forms.ModelForm):
    class Meta:
        model = models.Trapdoor
        fields = ['keyword']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "style": "width:200px", "placeholder": field.label}


def Trapdoor_gen(request):
    temp = models.Result.objects.last()
    if not temp:
        dispatch_index = 1
    else:
        dispatch_index = temp.index + 1
    queryset = models.IC.objects.filter(index=dispatch_index).all()
    message = "已有 " + str(len(queryset)) + " 个用户参与本轮调度"
    if request.method == "GET":
        form = TrapdoorModelForm()
        # disable_button = False
        if len(queryset) > 5:
            # form = ICModelForm(instance=queryset)自动显示内容
            return render(request, 'trapdoor_dispatch.html', {"form": form, "message": message})
        messages.add_message(request, messages.WARNING, "当前参与调度用户过少(需>5)，无法生成 trapdoor")
        disable_button = True
        return render(request, 'trapdoor_dispatch.html', {"disable_button": disable_button, "message": message})
    form = TrapdoorModelForm(request.POST)
    if form.is_valid():
        keyword = request.POST.get('keyword')
        Gsp = models.Gsp.objects.last()
        suppliers = []
        demanders = []
        st_max_demand = []
        st_demand_weight = []
        st_max_provide = []
        st_provide_weight = []
        print("调度人数:", len(queryset))
        for obj in queryset:
            # row_object是本轮调度中创建IC的Consumers对象
            row_object = models.Consumers.objects.filter(id=obj.userid_id).first()
            if row_object:
                row_object.status = "未参与本轮调度"
                row_object.save()
            SK_B1 = group.deserialize(Gsp.sk_B1)
            SK_B2 = group.deserialize(Gsp.sk_B2)
            PK_B1 = group.deserialize(Gsp.pk_B1)
            PK_B2 = group.deserialize(Gsp.pk_B2)
            PK_A1 = group.deserialize(row_object.b1)
            PK_A2 = group.deserialize(row_object.b2)
            SK_S = group.deserialize(Gsp.sk_s)
            IC1 = group.deserialize(obj.ic1)
            IC2 = group.deserialize(obj.ic2)
            lambda1 = group.hash((PK_A1, PK_B1, PK_A1 ** SK_B1))
            lambda2 = group.hash((PK_A2, PK_B2, PK_A2 ** SK_B2))
            ST_kw = group.hash((keyword, lambda1, lambda2), ZR) * SK_B1
            st = group.serialize(ST_kw)
            models.Trapdoor.objects.create(index=dispatch_index, keyword=keyword, st=st, userid_id=obj.userid_id)
            Q = IC1 ** (SK_S ** -1) * (IC1 ** ST_kw) ** (SK_S ** -1)
            if IC2 == group.hash(Q):
                power = round(float(obj.power), 2)
                priority = round(float(row_object.priority), 2)
                username = row_object.username
                # print(type(power), power)
                # 匹配成功将对应数据添加进数组
                # power = eval(obj.power)
                # 判断是需电还是供电
                if obj.type == 1:  # 供电
                    suppliers.append(username)
                    st_max_provide.append(power)
                    st_provide_weight.append(priority)
                else:  # 需电
                    demanders.append(username)
                    st_max_demand.append(power)
                    st_demand_weight.append(priority)
        suppliers = '[' + ','.join(map(str, suppliers)) + ']'
        demanders = '[' + ','.join(map(str, demanders)) + ']'
        a = len(st_demand_weight)
        b = len(st_provide_weight)
        total_demand = sum(st_max_demand)
        cap = round(sum(st_max_provide), 2)
        print("\n\n")
        print("有", a, "个需求用户")
        print("各自的用电要求分别是", st_max_demand)
        print("各自的权重分别是", st_demand_weight)
        print("有", b, "个供电用户")
        print("各自的最大供电量分别是", st_max_provide)
        print("各自的权重分别是", st_provide_weight)
        print("\n\n")
        print("总供电量是", round(cap, 2))
        print("总需电量是", round(total_demand, 2))
        st_true_provide, st_true_demand, _ = Pulp.pulp(st_max_provide, st_max_demand, st_provide_weight,
                                                       st_demand_weight)

        print("最后每个供电用户供给的电量为", st_true_provide)
        print("最后每个需求用户得到的电量为", st_true_demand)

        models.Result.objects.create(index=dispatch_index, suppliers=suppliers, demanders=demanders,
                                     supply=str(st_true_provide), demand=str(st_true_demand))
        for i in range(len(suppliers)):
            models.Consumers.objects.filter(username=suppliers[i]).update(
                remain_power=F('remain_power') - st_true_provide[i])
        for j in range(len(demanders)):
            models.Consumers.objects.filter(username=demanders[j]).update(
                remain_power=F('remain_power') + st_true_demand[j])
        return redirect('/result/' + str(dispatch_index) + '/info/')
    else:
        return render(request, 'trapdoor_dispatch.html', {'form': form, "message": message})
