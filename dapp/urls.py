"""
URL configuration for dapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.views.static import serve

from app01 import views
from app01.views import account, user, IndexCiphertextGen, SearchTrapdoorGen, result, chart
from django.conf import settings

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS}, name='static'),
    path('', account.login),
    path('login/', account.login),
    path('logout/', account.logout),
    path('index/', account.index),
    # path('user/list/',views.user_list),

    path('user/list/', user.User_list),
    path('user/add/', user.User_add),
    path('user/<int:nid>/edit/', user.User_edit),
    path('user/<int:nid>/info/', user.User_info),
    path('user/<int:nid>/dispatch/', IndexCiphertextGen.User_dispatch),
    path('user/delete/', user.User_delete),

    path("trapdoor/gen/", SearchTrapdoorGen.Trapdoor_gen),

    # path('index/ciphertext/', user.User_list),
    # path('index/<int:nid>/info/', user.User_info),

    path("result/<int:nid>/info/", result.Result_info),
    path('result/list/', result.Result_list),

    path('image/code/', account.image_code),

    path('chart/<int:nid>/supply1/', chart.chart_supply1),
    path('chart/<int:nid>/supply2/', chart.chart_supply2),
    path('chart/<int:nid>/demand1/', chart.chart_demand1),
    path('chart/<int:nid>/demand2/', chart.chart_demand2),
    path('chart/<int:nid>/line1/', chart.chart_line1),
    path('chart/<int:nid>/line2/', chart.chart_line2),
]
