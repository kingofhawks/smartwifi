from django.shortcuts import render, redirect, get_object_or_404, render_to_response, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.translation import ugettext as _
import json
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info, warning
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date, time, timedelta
from django.contrib.auth.models import User
from management.models import Gateway


def login(request):
    gw_address = request.GET.get('gw_address')
    gw_port = request.GET.get('gw_port')
    gw_id = request.GET.get('gw_id')
    mac = request.GET.get('mac')
    url = request.GET.get('url')

    #TODO

    return HttpResponse('OK', content_type="application/json")


def auth(request):
    stage = request.GET.get('stage')
    ip = request.GET.get('ip')
    mac = request.GET.get('mac')
    token = request.GET.get('token')
    incoming = request.GET.get('incoming')
    outgoing = request.GET.get('outgoing')

    #TODO
    data = {'Auth': 1}

    return HttpResponse(json.dumps(data), content_type="application/json")


def portal(request):
    stage = request.GET.get('stage')
    ip = request.GET.get('ip')
    mac = request.GET.get('mac')
    token = request.GET.get('token')
    incoming = request.GET.get('incoming')
    outgoing = request.GET.get('outgoing')

    #TODO

    return HttpResponse('OK', content_type="application/json")


def ping(request):
    gw_id = request.GET.get('gw_id')
    sys_uptime = request.GET.get('sys_uptime')
    sys_memfree = request.GET.get('sys_memfree')
    sys_memtotal = request.GET.get('sys_memtotal')

    gateway = get_object_or_404(Gateway, id=gw_id)

    data = {'ssid': gateway.ssid, 'authmode': 'open', 'password': '11111111', 'channel': 'test', 'pinginterval': 10}

    return HttpResponse(json.dumps(data), content_type="application/json")
