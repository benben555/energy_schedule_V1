from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01.utils.form import LoginForm
from app01.utils.verify import check_code
from app01 import models
from io import BytesIO


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            print(code.upper(), user_input_code.upper())
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {"form": form})
        # form.cleaned_data 验证成功
        # form。save（）是modelform有关联的数据库
        print(form.cleaned_data["password"])
        # admin_object=models.Admin.objects.filter(username=form.cleaned_data["username"],password=form.cleaned_data["password"]).first()
        admin_object = models.UserInfo.objects.filter(name=form.cleaned_data["username"],
                                                      password=form.cleaned_data["password"]).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")  # 主动显示错误
            return render(request, 'login.html', {"form": form})
        # 用户名和密码正确
        # 网站生成随机字符串，写到用户浏览器的cookie中，再写入到session中
        request.session['info'] = {"id": admin_object.id, "name": admin_object.name}
        # session保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/user/list/')
    return render(request, 'login.html', {"form": form})


def logout(request):
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    img, code_string = check_code()
    # 写入到自己到session中，以便后续获取验证码进行校验
    request.session['image_code'] = code_string

    # 设置60秒超时
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
