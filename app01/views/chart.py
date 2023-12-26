from django.http import JsonResponse
from django.shortcuts import render

from app01 import models


def chart_supply1(request, nid):
    legend = ["供电用户分别可供电量图"]
    row_object = models.Result.objects.filter(index=nid).first()
    suppliers = row_object.suppliers[1:-1].split(',')
    suppliers = [item.strip() for item in suppliers]
    # x_axis = {"data": suppliers}
    x_axis = suppliers
    max_supply = []
    for i in suppliers:
        consumer_object = models.Consumers.objects.filter(username=i).first()
        max_supply.append(models.IC.objects.filter(userid=consumer_object.id, index=nid).first().power)
    series_list = list(map(float, max_supply))
    result = {
        'status': True,
        "data": {
            'legend': legend,
            "series_list": series_list,
            "x_axis": x_axis
        }
    }
    return JsonResponse(result)


def chart_supply2(request, nid):
    legend = ["供电用户实际提供电量图"]
    row_object = models.Result.objects.filter(index=nid).first()
    suppliers = row_object.suppliers[1:-1].split(',')
    suppliers = [item.strip() for item in suppliers]
    # x_axis = {"data": suppliers}
    x_axis = suppliers
    supply = row_object.supply
    series_list = eval(supply)
    print(series_list)
    result = {
        'status': True,
        "data": {
            'legend': legend,
            "series_list": series_list,
            "x_axis": x_axis
        }
    }
    return JsonResponse(result)


def chart_demand1(request, nid):
    legend = ["需电用户所需电量图"]
    row_object = models.Result.objects.filter(index=nid).first()
    demanders = row_object.demanders[1:-1].split(',')
    demanders = [item.strip() for item in demanders]
    # x_axis = {"data": suppliers}
    x_axis = demanders
    max_demand = []
    for i in demanders:
        consumer_object = models.Consumers.objects.filter(username=i).first()
        max_demand.append(models.IC.objects.filter(userid=consumer_object.id, index=nid).first().power)
    series_list = list(map(float, max_demand))
    result = {
        'status': True,
        "data": {
            'legend': legend,
            "series_list": series_list,
            "x_axis": x_axis
        }
    }
    return JsonResponse(result)


def chart_demand2(request, nid):
    legend = ["需电用户实际得到电量图"]
    row_object = models.Result.objects.filter(index=nid).first()
    demanders = row_object.demanders[1:-1].split(',')
    demanders = [item.strip() for item in demanders]
    # x_axis = {"data": suppliers}
    x_axis = demanders
    demand = row_object.demand
    series_list = eval(demand)
    print(series_list)
    result = {
        'status': True,
        "data": {
            'legend': legend,
            "series_list": series_list,
            "x_axis": x_axis
        }
    }
    return JsonResponse(result)


def chart_line1(request, nid):
    row_object = models.Result.objects.filter(index=nid).first()
    suppliers = row_object.suppliers[1:-1].split(',')
    suppliers = [item.strip() for item in suppliers]
    x_axis = {"data": suppliers}
    suppliers_priority = []
    for i in suppliers:
        consumer_object = models.Consumers.objects.filter(username=i).first()
        suppliers_priority.append(consumer_object.priority)
    series_list = {"data": suppliers_priority}
    result = {
        'status': True,
        "series_list": series_list,
        "x_axis": x_axis
    }
    return JsonResponse(result)


def chart_line2(request, nid):
    row_object = models.Result.objects.filter(index=nid).first()
    demanders = row_object.demanders[1:-1].split(',')
    demanders = [item.strip() for item in demanders]
    x_axis = {"data": demanders}
    demanders_priority = []
    for i in demanders:
        consumer_object = models.Consumers.objects.filter(username=i).first()
        demanders_priority.append(consumer_object.priority)
    series_list = {"data": demanders_priority}
    result = {
        'status': True,
        "series_list": series_list,
        "x_axis": x_axis
    }
    return JsonResponse(result)
