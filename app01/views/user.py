import random
from charm.core.math.elliptic_curve import ZR
from django import forms
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from charm.toolbox.eccurve import prime192v2
from charm.toolbox.ecgroup import ECGroup

group = ECGroup(prime192v2)


class UserModelForm(forms.ModelForm):
    # name = forms.CharField(min_length=3, label="用户名") 加上校验
    # name = forms.CharField(label="用户名",validators=) 正则表达式
    class Meta:
        model = models.Consumers
        fields = ['username', 'phone']
        # widgets = {
        #     "a1": forms.TextInput(
        #         attrs={"type": "password", "autocomplete": "off"}),
        #     "a2": forms.TextInput(
        #         attrs={"type": "password", "autocomplete": "off"}),
        # }
        # 循环找到所有的插件 加上样式

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "style": "width:150px", "placeholder": field.label}


def User_list(request):
    info_dict = request.session['info']
    name = info_dict['name']
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data
    print("data:  " + search_data)
    queryset = models.Consumers.objects.filter(**data_dict)
    temp = models.Consumers.objects.exclude(status="未参与本轮调度")
    message = "已有 " + str(len(temp)) + " 个用户参与本轮调度"
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
        "message": message
    }
    # queryset = models.Consumers.objects.all()
    # 用户上传时间obj.create_time.strftime('%Y-%m-%d %H:%M' )  type(obj.create_time)
    # 模板语言不允许加括号 queryset.get_gender_display；obj.create_time|date: 'Y-m-d H:i'
    # a=queryset[0].get_type_display()
    # content={
    #     "gender":models.Consumer.type_choices
    # }
    return render(request, 'user_list.html', context)


def User_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add.html', {'form': form})
    form = UserModelForm(request.POST)
    if form.is_valid():
        Gsp = models.Gsp.objects.first()
        P = group.deserialize(Gsp.p)
        # form.save()  # 自动保存数据库
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        priority = "%.2f" % (random.random() + random.randint(0, 9))
        Id = models.Consumers.objects.last()
        if not Id:
            name = 1
        else:
            name = Id.id + 1
        a11 = request.POST.get("a1")
        sk_A1 = group.hash(a11 + str(name), ZR)
        a1 = group.serialize(sk_A1)
        a22 = request.POST.get("a2")
        if a11 == a22:
            a22 += str(name)
        sk_A2 = group.hash(a22 + str(name), ZR)
        a2 = group.serialize(sk_A2)
        # str1 = gsp.group.zr(sk_A1)
        # str2 = gsp.group.zr(sk_A2)
        b1 = P ** sk_A1
        sb1 = str(b1)
        b1 = group.serialize(b1)
        b2 = P ** sk_A2
        sb2 = str(b2)
        b2 = group.serialize(b2)
        models.Consumers.objects.create(username=username, phone=phone, remain_power=0, a1=a1, a2=a2, b1=b1, sb1=sb1,
                                        b2=b2, sb2=sb2, priority=priority)
        return redirect('/user/list/')
    else:
        return render(request, 'user_add.html', {'form': form})


def User_info(request, nid):
    if request.method == "GET":
        row_object = models.Consumers.objects.filter(id=nid).first()
        return render(request, 'user_info.html', {"row_object": row_object})
    return redirect('/user/list/')


def User_delete(request):
    nid = request.GET.get('nid')
    models.Consumers.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def User_edit(request, nid):
    if request.method == "GET":
        row_object = models.Consumers.objects.filter(id=nid).first()
        return render(request, 'user_edit.html', {"row_object": row_object})
    priority = request.POST.get("priority")
    phone = request.POST.get("phone")
    username = request.POST.get("username")
    remain_power = request.POST.get("remain_power")
    models.Consumers.objects.filter(id=nid).update(username=username, priority=priority, phone=phone,
                                                   remain_power=remain_power)
    return redirect('/user/list/')
