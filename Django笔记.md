## Django默认项目

> mysite
>
> |--manage.py      【项目管理，启动项目、创建APP、数据管理】
> |--mysite 
> ​      |--_init_.py
> ​      |--settings.py   【项目配置 】
> ​      |--urls.py          【URL和函数的对应关系】 
> ​      |--asgi.py          【接受网络请求（异步）】
> ​      |--wsgi.py         【接受网络请求（同步）】



## APP

> -大型项目
> ——app,用户管理【独立的表结构、函数、HTML模板、css】
> ——app,订单管理【独立的表结构、函数、HTML模板、css】
> ——app,后台管理【独立的表结构、函数、HTML模板、css】
> ——app,网站        【独立的表结构、函数、HTML模板、css】
> ——app,API          【独立的表结构、函数、HTML模板、css】

 

>|--app01
>|        |--_init_.py
>|        |--admin.py            【固定不动】django默认提供了admin后台管理
>|        |--apps.py               【固定不动】app启动类
>|        |--migration.py      【固定不动】数据库变更记录
>|                   |--_init_.py
>|        |--models.py          【对数据库进行操作】
>|        |--tests.py               【固定不动】单元测试
>|        |--views.py              【放置URL中定义的函数】
>|--manage.py
>|--mysite2
>     |--_init_.py
>     |--asgi.py
>     |--settings.py
>     |--urls.py               【URL->函数】
>     |--wsgi.py



## 快速上手

- 确保APP已注册（settings.py中）

- ```
  INSTALLED_APPS = [
  'ChemDataManager.apps.ChemdatamanagerConfig'
  ]
  ```

- 编写URL和视图函数的对应关系(urls.py)

- ```
  from django.urls import path
  from ChemDataManager import views
  urlpatterns = [
     # path('admin/', admin.site.urls),链接路径和函数
       path('index/', views.index ),
  ]
  ```

- 编写视图函数（views.py）

- ```
  from django.shortcuts import render,HttpResponse
  def index(request):
      #request是默认参数
      return HttpResponse("成功访问")
  ```

- 启动项目

​       命令行启动

​       Pycharm启动



## 添加页面

```
-url _> 函数
函数
```



## template模板

```
from django.shortcuts import render,HttpResponse
def index(request):
    #request是默认参数
    return HttpResponse("成功访问")

def users_list(request):
    # 去app目录下templates目录寻找目标html(顺序遍历每个app目录templates搜索，预先配置html)
    return render(request,"users_list.html")

def users_add(request):
    return HttpResponse("添加用户")
```



## 静态文件

开发过程中

- 图片

- CSS

- js

  都当作静态文件处理





1. app目录下创建static文件夹

    app-staic-css/js/img/plugins

   

2. 引用静态文件

   ```
   {% load static %}
   "{% static 'plugins/boostrap-3.4.1/css/boorstrap.css' %}"
   ```



## 模板语法(Django)

本质上：HTML中写一些占位符，由数据对占位符进行替换处理





### 案例：



## 请求和响应

### 案例：用户登录



## 数据库操作

- mysql数据库+pymysql

  

```python
import pymysql

# 1.连接mysql
conn=pymysql.connect(host="127.0.0.1",port=3306,user='root'
passwd="root123",charset='utf8',db='unicom')
cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)

# 2.发送指令
cursor.execute("insert into admin(username,password,mobile)
values('lubenwei','benzema','caixukun')")
conn.commit()

# 3.关闭
cursor.close()
conn.colse
```



- Django开发操作数据库更为简化，内部集成了ORM框架，作中间层，方便移植

  

## 安装第三方模块

```
pip install mysqlclient
```





## ORM

ORM可以

- 创建、修改、删除数据库中的表【无法创建数据库】

- 操作表中数据【不用写sql语句】

  ```py
  insert into...
  update
  select..
  ```



### 自己创建数据库

- 启动MySQL服务
- 自带工具创建数据库

```python
create database dbOne DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```





## Django操作表

- 创建表
- 删除表
- 修改表

创建表，在model.py中

```
create table ChemDataManager_userinfo(
    id bigint auto_increment primary key,
    name varchar(32)
    password varchar(64)
    age int
)
```

执行命令：（app需在settings中注册）

``` 
python manage.py makemigrations
python manage.py migrate

```





在表中新增列时，由于已存在的列中可能已有数据，所以新增列必须要指定新增列对应的数据：

- 1.手动输入一个值

- 2.设置默认值

  ```
  age = models.IntegerField(default=2)
  ```

- 3.允许为空

  ```
  data = models.IntegerField(null=True,blank=True)
  ```
  



以后在开发中如果想要对表结构进行调整：

- 在models.py文件中操作类即可
- 再次运行命令

``` 
python manage.py makemigrations
python manage.py migrate

```





## 表中的数据

```
# 新建
# models.Department.objects.create(title="销售")
# models.Department.objects.create(title="IT")
# models.Department.objects.create(title="运营")
#
# models.UserInfo.objects.create(name="卢本伟",password="111222",age="22")
# models.UserInfo.objects.create(name="pdd",password="114514",age="17")

# 删除
# models.Department.objects.filter(title="IT").delete()
# models.UserInfo.objects.all().delete()
# models.Department.objects.all().delete()


# 获取限定条件的数据
# data_list=[行，行，行]  QuerySet类型
data_list=models.UserInfo.objects.all()
# for object in data_list:
#     print(object.id,object.name,object.password,object.age)
# return HttpResponse("success")


# 获取第一条数据
# row_obj=models.UserInfo.objects.filter(id=20).first()
# print(row_obj.id,row_obj.name,row_obj.password,row_obj.age)
# return HttpResponse("success")

# 更新数据
# models.UserInfo.objects.all().update(password=1999)
# models.UserInfo.objects.filter(name="pdd").update(password=666)
# return HttpResponse("success")
```





## 案例：用户管理

1. 展示用户列表
   - url
   - 函数
     - 获取所有用户信息
     - HTML渲染



2. 添加用户
  - url
  - 函数
    - GET,看到页面，输入内容
    - POST,提交->写入到数据库
3. 删除用户

  	- url
  	- 函数



``` 
http://127.0.0.1:8000/info/delete/?nid=1
http://127.0.0.1:8000/info/delete/?nid=2
http://127.0.0.1:8000/info/delete/?nid=3

def 函数(request):
	nid = request.GET.get("nid")
	UserInfo.objects.filter(id=nid).delete()
	return Http Response ("shan'chu'che")
```





# Django开发



1. 新建项目

​		删除settings.py中 DIRS中内容

```
TEMPLATES = [
     'DIRS': []
```

​		删除templates文件夹



2. 创建app

​		命令行输入 python manage.py startapp appNAME



3. 注册app

​		settings.py中INSTALLED_APPS中添加

``` 
"appNAME.apps.App01Config"
```



4. 设计表结构

```
#无约束，无法关联id表
# depart_id = models.BigAutoField(verbose_name="部门ID")

#有约束
#to关联表，to_fields关联列
#django自动:写的depart，生成数据列”depart_id“

#当部门表被删除
#A.级联删除(删除对应部门用户)
# depart = models.ForeignKey(to="Department",to_field="id",on_delete=models.CASCADE)
#B.置空(用户部门id清空)
# depart = models.ForeignKey(to="Department",to_fields="id",null=True,blank=True,on_delete=models.SET_NULL)
```





5. 在MySQL中生成表

``` 
create database app01_database DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

 修改setting文件连接MySQL

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'app01_database',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}
```



django命令生成数据库表

``` python
python manage.py makemigrations
python manage.py migrate
```





6. 静态文件管理

"New folder "static","templates"

7. 部门管理

   > 原始方法
   >
   > Django中亦提供Form和ModelForm组件(方便)

- 部门列表

		- 页面设计
		- 





Django中使用POST，需要输入

```html
{% csrf_token %}
```





## 模板的继承

- 部门列表
- 添加部门
- 编辑部门



定义母版:layout.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
     <link rel="stylesheet" href="{% static 'plugins...min.css' %}">
    {% block css %}{% endblock %}
</head>
<body>
	<h1>标题</h1>
	<div>
   		 {% block content %} {% endblock %}
	</div>
	<h1>底部</h1>
    
    <script src="{% static 'js/jquery-3.6.0.min.js' %}"></script>
    {% block js%}{% endblock %}
</body>
</html>
```



继承母版:

```html
{% extends 'layout.html' %}

{% block css %}
	<link rel="stylesheet" href="{% static 'pluxxx.css' %}">
	<style>
		...
	</style>
{% endblock %}

{% block content %}
    <h1>首页</h1>
{% endblock %}


{% block js %}
	<script src="{% static 'js/jqxxx.js' %}"></script>
{% endblock %}
```





## 用户管理

```mysql
insert into app01_userinfo(name,password,age,account,create_time,gender,depart_id)
values("张伟","123",23,100.68,"2022-10-29",1,2);

insert into app01_userinfo(name,password,age,account,create_time,gender,depart_id)
values("王伟","456",24,1000.68,"2022-10-30",1,5);

insert into app01_userinfo(name,password,age,account,create_time,gender,depart_id)
values("李伟","789",25,10000.68,"2022-10-31",2,6);
```




```sql
+-------------+---------------+------+-----+---------+----------------+
| Field       | Type          | Null | Key | Default | Extra          |
+-------------+---------------+------+-----+---------+----------------+
| id          | bigint        | NO   | PRI | NULL    | auto_increment |
| name        | varchar(16)   | NO   |     | NULL    |                |
| password    | varchar(64)   | NO   |     | NULL    |                |
| age         | int           | NO   |     | NULL    |                |
| account     | decimal(10,2) | NO   |     | NULL    |                |
| create_time | datetime(6)   | NO   |     | NULL    |                |
| gender      | smallint      | NO   |     | NULL    |                |
| depart_id   | bigint        | NO   | MUL | NULL    |                |
+-------------+---------------+------+-----+---------+----------------+
```



执行插入后：

```sql
+----+------+----------+-----+----------+----------------------------+--------+-----------+
| id | name | password | age | account  | create_time                | gender | depart_id |
+----+------+----------+-----+----------+----------------------------+--------+-----------+
|  3 | 张伟 | 123      |  23 |   100.68 | 2022-10-29 00:00:00.000000 |      1 |         2 |
|  4 | 李伟 | 789      |  25 | 10000.68 | 2022-10-31 00:00:00.000000 |      2 |         6 |
|  5 | 王伟 | 456      |  24 |  1000.68 | 2022-10-30 00:00:00.000000 |      1 |         5 |
+----+------+----------+-----+----------+----------------------------+--------+-----------+
```





## 新建用户



- 原始方法理思路：
  - 用户提交的数据没有校验
  - 错误，页面上应有提示
  - 页面上，每一个字段都需要重写
  - 关联的数据，需要手动获取并展示循环在页面上

- Django组件：
  - Form组件
  - ModelForm组件





## 初识Form



1. views.py

   ```py
   class MyForm(Django中的.Form)
   	user = forms.CharField(widge=form.Input)
       pwd  = form.CharField(widge=form.Input)
       email = form.EmailField(widge=form.Input)
   
   def user_add(request):
       if request.method == "GET":
           form = MyForm()
           return render(request,'user_add.html',{"form":form})
   ```

   

2. user_add.html

   ```py
   <form method="POST">
   	{{form.user}}
   	{{form.pwd}}
   	{{form.email}}
   
       替代以下传统代码
       <!-- <input type="text" class="form-control" placeholder="姓名" name="user"> -->
             <input type="text" class="form-control" placeholder="姓名" name="user">
             <input type="text" class="form-control" placeholder="姓名" name="user">       
               
   循环写法
   
   <form method="POST">
   	{% for field in form %}
       	{{ field }}
       {% endfor %}
   </form>
   ```





## ModelForm(推荐)



1. models.py

```py
class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名",max_length=16)
    password = models.CharField(verbose_name="密码",max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额",max_digits=10,decimal_places=2,default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")

    
    depart = models.ForeignKey(to="Department",to_field="id",on_delete=models.CASCADE)
   
    gender_choices = (
        (1,"男"),
        (2,"女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)
```



2. views.py

```py
class MyForm(ModelForm)
	class Meta:
        model = UserInfo
        fileds = ["name","password","age","account","create_time","depart","gender"]

def user_add(request):
    if request.method == "GET":
        form = MyForm()
        return render(request,'user_add.html',{"form":form})
```



3. user_add.html

```py
<form method="POST">
	{{form.user}}
	{{form.pwd}}
	{{form.email}}

    替代以下传统代码
    <!-- <input type="text" class="form-control" placeholder="姓名" name="user"> -->
          <input type="text" class="form-control" placeholder="姓名" name="user">
          <input type="text" class="form-control" placeholder="姓名" name="user">       
            
循环写法

<form method="POST">
	{% for field in form %}
    	{{ field }}
    {% endfor %}
</form>
```



ModelForm展示页面

```
<form method="post" novalidate>
             {% csrf_token %}
             {% for field in form %}
                 <div class="form-group">
                    <label>{{ field.label }}:</label>
{#                    <input type="text" class="form-control" placeholder="姓名" name="user">#}
                    {{ field }}
                     <span style="color: red;">
                    {{ field.errors.0 }}
                     </span>
                 </div>
             {% endfor %}


             <button type="submit" class="btn btn-primary">提 交</button>
         </form>
```

ModelForm操作数据库、数据校验

```
form = UserModelForm(data=request.POST)
if form.is_valid():
    #如果数据合法，保存到数据库(ModelForm方法)
    # print(form.cleaned_data)
    form.save()
    return redirect('/user/list/')

    #校验失败(在页面上写错误信息)
return render(request,'user_model_form_add.html',{"form":form})
```







## 编辑用户

- 点击编辑跳转编辑页面，并把当前ID传递

- 编辑页面（默认数据，根据ID获取放置在页面中）

- 提交

  - 数据校验

  - 错误提示

  - 数据库更新

    ```py
    models.UserInfo.filter(id=4).update(...)# 传统方法
    
    ```
    
    ModelForm方法
    

```py
def user_edit(request,nid):
    """编辑用户"""
    #根据ID去数据库获取要编辑的那一行数据（对象）
    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(instance=row_object)
    return render(request,'user_edit.html',{"form":form})
```





## 删除用户 

```py
def user_delete(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')

```

总需电量总供电量



请选择用哪种算法优先级

# 靓号管理



数据库的表结构

| id   | mobile | level（choices） | price | status（占用） |
| ---- | ------ | ---------------- | ----- | -------------- |
|      |        |                  |       |                |
|      |        |                  |       |                |
|      |        |                  |       |                |

在model.py中创建类（由类生成数据库的表）

```py
class PrettyNum(models.Model):
 
```



自己在数据库模拟创建一些数据

```sql
insert
```

用户当前电量请输入大小请选择操作买入卖出请确认提交需电用户列表供电用户列表



## 靓号列表

- URL

- 函数

  - 获取所有靓号
  - 结合html+render展示所有靓号

  | ID   | 号码 | 价格 | 级别 | 状态 |
  | ---- | ---- | ---- | ---- | ---- |





## 新建靓号

- 列表点击跳转: /pretty/add/

- URL

- ModelForm类

  ```py
  from django import forms
  
  class prettyModelForm(forms.ModelForm):
      
  ```

  

- 函数

  - 实例化类的对象
  - 通过render将对象传入到HTML中
  - 通过循环展示所有的字段

- 点击提交

  - 数据校验
  - 保存到数据库
  - 跳转回靓号list



不允许手机号重复

- 添加：【正则表达式】 【手机号不能重复】

```py
queryset = models.PrettyNum.objects.filter(mobile="18888888888")

obj = models.PrettyNum.objects.filter(mobile="18888888888").first()

#exists方法 结果为True/False
exists = models.PrettyNum.objects.filter(mobile="18888888888").exists()
```





## 编辑靓号

- 列表页面：pretty/数字/edit

- URL
- 函数
  - 根据ID获取当前编辑对象
  - ModelForm配合，默认显示数据
  - 提交修改

  





- 编辑：【正则表达式】【手机号不能重复】
- 排除自己以外，与其他的手机号是否重复


```py
# id!=2 and mobile='18888'
exists = models.PrettyNum.objects.filter(mobile="18888888888").exclude(id=2 )
```





# 搜索手机号

```python
普通方法
models.PrettyNum.objects.filter(mobile="15534065210",id=1)

字典方法
data_dict = {"mobile":"15534065210","id":1}
models.PrettyNum.objects.filter(**data_dict)
```





```python
models.PrettyNum.objects.filter(id=12) 					#等于12
models.PrettyNum.objects.filter(id__gt=12)				#大于12	
models.PrettyNum.objects.filter(id__gte=12)				#大于等于12
models.PrettyNum.objects.filter(id__lt=12)				#小于12
models.PrettyNum.objects.filter(id__lte=12)				#小于等于12

data_dict = {"id__lte":12}								#和字典联用
models.PrettyNum.objects.filter(**data_dict)			#小于等于12


models.PrettyNum.objects.filter(mobile="155")				#等于155
models.PrettyNum.objects.filter(mobile__startswith="155")	#筛选出以155开头
models.PrettyNum.objects.filter(mobile__endswith="155")		#筛选出以155结尾
models.PrettyNum.objects.filter(mobile__contains="155")		#筛选出包含155

data_dict = {"mobile__contains":"155"}					#和字典联用
models.PrettyNum.objects.filter(**data_dict)				#筛选出包含155	
```





# 分页

```py
queryset = models.PrettyNum.objects.all()

queryset = models.PrettyNum.objects.filter[0:10]

第一页
queryset = models.PrettyNum.objects.all[0:10]  #取前10数据
第二页
queryset = models.PrettyNum.objects.all[10:20]  
第三页
queryset = models.PrettyNum.objects.all[20:30]  

```



# 时间



```
<script src="{% static 'plugins/bootstrap-datepicker-master/dist/js/bootstrap-datepicker.js' %}"></script>
<script src="{% static 'plugins/bootstrap-datepicker-master/js/locales/bootstrap-datepicker.zh-CN.js' %}"></script>
```

 

# ModelForm和BootStrap

- ModelForm生成HTML时

```
class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name","password","age","account","create_time","gender","depart"]
```

- 定义插件

- 

 ```python
  class UserModelForm(forms.ModelForm):
      name = forms.CharField(min_length=3,label="用户名")
  
      class Meta:
          model = models.UserInfo
          fields = ["name","password"]
           widgets = {
             "name":forms.TextInput(attrs={"class":"form-control"}),
             "password": forms.PasswordInput(attrs={"class": "form-control"}),    
       }
 ```

```py
class UserModelForm(forms.ModelForm):
    name = forms.CharField(
        min_length=3,
        label="用户名",
    	widget=form.TextInput(attrs={"class":"formn-control"})
     )

    class Meta:
        model = models.UserInfo
        fields = ["name","password"]

```

- 重新定义的init方法，批量设置

```py
class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3,label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name","password","age"]
      

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
         
            #循环找到所有插件，添加class=form-control
        for name, field in self.fields.items():
         field.widget.attrs = {"class":"form-control",
                               "placeholder":field.label
                              }
```

```py
class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3,label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name","password","age"]
      

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
         
        #循环找到所有插件，添加class=form-control
        for name, field in self.fields.items():
            
            #字段中有属性，保留原属性，没有属性则增加属性
            if field.widge.attrs:
                field.widget.attrs["class"]="form-control"
                field.widget.attrs["placeholder"]=field.label
            else:
         		field.widget.attrs = {
                    "class":"form-control",
                    "placeholder":field.label
                              }
```

- 自定义类

```py
class BootStrapModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)  
        #循环找到所有插件，添加class=form-control
        for name, field in self.fields.items():
            #字段中有属性，保留原属性，没有属性则增加属性
            if field.widge.attrs:
                field.widget.attrs["class"]="form-control"
                field.widget.attrs["placeholder"]=field.label
            else:
         		field.widget.attrs = {
                    "class":"form-control",
                    "placeholder":field.label
                              }
```

```py
class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name","password","age"]
      
```



- 管理员操作
