from charm.core.math.elliptic_curve import ZR
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from app01 import models
from charm.toolbox.eccurve import prime192v2
from charm.toolbox.ecgroup import ECGroup

group = ECGroup(prime192v2)


class ICModelForm(forms.ModelForm):
    # b1=forms.CharField(disabled=True,label="用户名")) display but not edit
    class Meta:
        model = models.IC
        fields = ['keyword', 'type', 'power']

    # def clean_power(self, nid):
    #     power = "%.2f" % float(self.cleaned_data['power'])
    #     remain_power = "%.2f" % float(models.Consumers.objects.exclude(id=nid).first().remain_power)
    #     if self.cleaned_data['type'] == "1":
    #         if power > remain_power:
    #             raise ValidationError("您当前剩余电量不足提供这么多")


def User_dispatch(request, nid):
    user_info = ICModelForm()
    row_object = models.Consumers.objects.filter(id=nid).first()
    # disable_button = True
    if request.method == "GET":
        # temp = models.Consumers.objects.filter(id=nid).first()
        if row_object.status == "未参与本轮调度":
            # form =
            # form = ICModelForm(instance=queryset)自动显示内容
            return render(request, 'user_dispatch.html', {'form': user_info, "row_object": row_object})
        return redirect('/user/list/')
    form = ICModelForm(request.POST)
    if form.is_valid():
        # form.save()  # 自动保存数据库
        # a11 = request.POST.get('a1')
        # a12 = request.POST.get('a2')
        # # 首先将输入的字符串扩充至20位，然后encode编码成bytes类型，再编码成elliptic_curve.Element类型
        # a11 = request.POST.get("a1")
        # a1 = a11.zfill(20)
        # temp = a1.encode('utf-8')
        # sk_A1 = group.encode(temp)  # group element类型[x,y]
        #
        # a2 = a12.zfill(20)
        # temp = a2.encode('utf-8')
        # sk_A2 = group.encode(temp)  # group element类型[x,y]
        #
        # a1 = group.zr(sk_A1)  # x
        # a2 = group.zr(sk_A2)  # x

        row_object = models.Consumers.objects.filter(id=nid).first()
        Gsp = models.Gsp.objects.first()
        P = group.deserialize(Gsp.p)
        keyword = request.POST.get('keyword')
        power = request.POST.get('power')
        power = round(float(power), 2)
        role = request.POST.get('type')
        status = "已参与本轮调度    "
        if role == "1":
            status += "可提供:" + str(power) + "°电"
            if power > round(float(row_object.remain_power), 2):
                disable_button = False
                messages.add_message(request, messages.WARNING, "您当前剩余电量不足提供这么多")
                print("false")
                return render(request, 'user_dispatch.html',
                              {'form': form, "disable_button": disable_button, "row_object": row_object})
        else:
            status += "需要:" + str(power) + "°电"
        a1, a2 = row_object.a1, row_object.a2
        sk_A1 = group.deserialize(a1)
        sk_A2 = group.deserialize(a2)
        b1, b2 = row_object.b1, row_object.b2
        pk_A1 = group.deserialize(b1)
        pk_A2 = group.deserialize(b2)
        pk_B1 = group.deserialize(Gsp.pk_B1)
        pk_B2 = group.deserialize(Gsp.pk_B2)
        lambda1 = group.hash((pk_A1, pk_B1, pk_B1 ** sk_A1))
        lambda2 = group.hash((pk_A2, pk_B2, pk_B2 ** sk_A2))

        r = group.random(ZR)
        pk_s = group.deserialize(Gsp.pk_s)

        q = P ** r * (pk_B1 ** group.hash((keyword, lambda1, lambda2))) ** r
        ic1 = pk_s ** r
        IC1 = group.serialize(ic1)
        ic2 = group.hash(q)
        IC2 = group.serialize(ic2)
        temp = models.Result.objects.last()
        if not temp:
            dispatch_index = 1
        else:
            dispatch_index = temp.index + 1
        models.IC.objects.create(keyword=keyword, userid_id=nid, ic1=IC1,
                                 ic2=IC2, power=power, type=role, index=dispatch_index)
        models.Consumers.objects.filter(id=nid).update(status=status)
        return redirect('/user/list/')
    else:
        return render(request, 'user_dispatch.html', {'form': form})
