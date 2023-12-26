import ast

from django.db.models import Q

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from django.shortcuts import render, redirect

from app01.utils.pagination import Pagination


class ResultModelForm(BootStrapModelForm):
    class Meta:
        model = models.Result
        fields = "__all__"


def Result_list(request):
    search_data = request.GET.get('q', "")
    queryset = models.Result.objects.filter(Q(suppliers__contains=search_data) | Q(demanders__contains=search_data))
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, 'result_list.html', context)


def Result_info(request, nid):
    if request.method == "GET":
        row_object = models.Result.objects.filter(index=nid).first()
        suppliers = row_object.suppliers[1:-1].split(',')
        suppliers=[item.strip() for item in suppliers]
        # suppliers = ast.literal_eval(row_object.suppliers)  # 优先级
        demanders = row_object.demanders[1:-1].split(',')
        demanders = [item.strip() for item in demanders]
        max_supply = []
        max_demand = []
        suppliers_priority = []
        demanders_priority = []
        for i in suppliers:
            consumer_object = models.Consumers.objects.filter(username=i).first()
            suppliers_priority.append(consumer_object.priority)
            max_supply.append(models.IC.objects.filter(userid=consumer_object.id, index=nid).first().power)
        for i in demanders:
            consumer_object = models.Consumers.objects.filter(username=i).first()
            demanders_priority.append(consumer_object.priority)
            max_demand.append(models.IC.objects.filter(userid=consumer_object.id, index=nid).first().power)
        return render(request, 'result_info.html',
                      {"row_object": row_object, "suppliers_priority": list(map(float, suppliers_priority)),
                       "suppliers_power": list(map(float, max_supply)),
                       "demanders_priority": list(map(float, demanders_priority)),
                       "demanders_power": list(map(float, max_demand))})
    return redirect('/result/list/')
