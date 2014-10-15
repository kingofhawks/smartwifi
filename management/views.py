from django.shortcuts import render, redirect, get_object_or_404, render_to_response, get_list_or_404
from models import (Notification, Gateway, WifiClient, Ad, AdStat, SmsTemplate)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from forms import (NotificationForm)
from django.utils.translation import ugettext as _
import json
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info, warning
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.core import serializers
#json.dumps do not work with DateTime object type,need to use DjangoJSONEncoder
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date, time, timedelta
from django.contrib.auth.models import User


class GatewayList(ListView):
    model = Gateway
    template_name = 'gateway_list.html'
    context_object_name = 'gateways'


class GatewayCreate(CreateView):
    model = Gateway
    template_name = 'create_project.html'

    success_url = reverse_lazy('management.gateways')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GatewayCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = _('Create')
        return context


class GatewayUpdate(UpdateView):
    model = Gateway
    template_name = 'create_project.html'
    success_url = reverse_lazy('management.gateways')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GatewayUpdate, self).get_context_data(**kwargs)
        # Add extra context variable
        context['title'] = _('Modify Gateway')
        return context


class GatewayDelete(DeleteView):
    model = Gateway
    template_name = 'gateway_confirm_delete.html'
    success_url = reverse_lazy('management.gateways')


class WifiClientList(ListView):
    model = WifiClient
    template_name = 'client_list.html'
    context_object_name = 'clients'


class AdList(ListView):
    model = Ad
    template_name = 'ad_list.html'
    context_object_name = 'ads'


class AdDetail(DetailView):
    model = Ad
    template_name = 'ad_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AdDetail, self).get_context_data(**kwargs)

        #Create AD stats record
        print self.object
        stat = AdStat(ad=self.object, showtime=datetime.today())
        stat.save()

        return context


class AdCreate(CreateView):
    model = Ad
    template_name = 'create_project.html'

    success_url = reverse_lazy('management.ads')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AdCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = _('Create')
        return context


class AdUpdate(UpdateView):
    model = Ad
    template_name = 'create_project.html'
    success_url = reverse_lazy('management.ads')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AdUpdate, self).get_context_data(**kwargs)
        # Add extra context variable
        context['title'] = _('Modify Ad')
        return context


class AdDelete(DeleteView):
    model = Ad
    template_name = 'gateway_confirm_delete.html'
    success_url = reverse_lazy('management.ads')


class AdStatsList(ListView):
    model = AdStat
    template_name = 'ad_stats_list.html'
    context_object_name = 'stats'

    def get_queryset(self):
        mode = self.request.GET.get('mode')
        print 'mode:{}'.format(mode)
        if mode is None or mode == 'today':
            today_min = datetime.combine(date.today(), time.min)
            today_max = datetime.combine(date.today(), time.max)
            print type(today_min)
            print today_min, today_max
            return AdStat.objects.filter(showtime__range=(today_min, today_max))
        elif mode == 'yesterday':
            d = date.today() - timedelta(days=1)
            today_min = datetime.combine(d, time.min)
            today_max = datetime.combine(d, time.max)
            print today_min, today_max
            return AdStat.objects.filter(showtime__range=(today_min, today_max))
        elif mode == 'last7Days':
            d = date.today() - timedelta(days=7)
            today_min = datetime.combine(d, time.min)
            today_max = datetime.combine(date.today(), time.max)
            print today_min, today_max
            return AdStat.objects.filter(showtime__range=(today_min, today_max))
        elif mode == 'month':
            today = date.today()
            print today.day
            d = today - timedelta(days=today.day-1)
            today_min = datetime.combine(d, time.min)
            today_max = datetime.combine(today, time.max)
            print today_min, today_max
            return AdStat.objects.filter(showtime__range=(today_min, today_max))
        elif mode == 'search':
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            start_date = datetime.strptime(start, '%Y-%m-%d')
            end_date = datetime.strptime(end, '%Y-%m-%d')
            print '{}:{}'.format(start, end)
            print '{}:{}'.format(start_date, end_date)
            today_min = datetime.combine(start_date, time.min)
            today_max = datetime.combine(end_date, time.max)
            print today_min, today_max
            return AdStat.objects.filter(showtime__range=(today_min, today_max))


            # Invoice.objects.get(user=user, date__range=(today_min, today_max))
        return AdStat.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AdStatsList, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        # context['title'] = _('Create')
        # from django.core import serializers
        # stats_json = serializers.serialize('json', self.get_queryset())
        # # context['stats_json'] = stats_json
        # print stats_json
        import pandas as pd
        #create pandas DF from Django QuerySet
        df = pd.DataFrame.from_records(self.get_queryset().values())
        print df
        count = len(df.index)
        print 'count:{}'.format(count)

        mode = self.request.GET.get('mode') or 'today'
        json_data = []
        stats = {}
        if count != 0:
            print 'mode:{}'.format(mode)
            df.time = pd.to_datetime(df.showtime, unit='s')
            df.set_index('showtime', inplace=True)
            # volume = df['count'].resample('D', how='sum')
            volume = df['count'].resample('D', how='sum')
            if mode == 'today' or mode == 'yesterday':
                volume = df['count'].resample('60Min', how='sum')
            print volume
            volume.fillna(0)
            json_data = volume.reset_index().to_json(date_format='iso', orient='records')
            print json_data
            # print type(js)
            df2 = volume.reset_index()
            # df2.fillna(0)
            print df2
            stats = df2.to_dict('records')
            print stats
            # print volume.reset_index().as_matrix()

            # data = json.dumps(js)
            # print data
            # print type(data)

        # context['stats'] = stats
        context['stats_json'] = json_data
        context['mode'] = mode

        return context


class SmsTemplateList(ListView):
    model = SmsTemplate
    template_name = 'sms_template_list.html'
    context_object_name = 'templates'


class SmsTemplateCreate(CreateView):
    model = SmsTemplate
    template_name = 'create_project.html'

    success_url = reverse_lazy('management.templates')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SmsTemplateCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = _('Create')
        context['model_name'] = _('SMS Templates')
        return context


class SmsTemplateUpdate(UpdateView):
    model = SmsTemplate
    template_name = 'create_project.html'
    success_url = reverse_lazy('management.templates')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SmsTemplateUpdate, self).get_context_data(**kwargs)
        # Add extra context variable
        context['title'] = _('Modify SMS Template')
        return context


class SmsTemplateDelete(DeleteView):
    model = SmsTemplate
    template_name = 'gateway_confirm_delete.html'
    success_url = reverse_lazy('management.templates')


class NotificationList(ListView):
    model = Notification
    template_name = 'notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        print self.request.user
        groups = self.request.user.groups.values_list('name', flat=True)
        print groups
        if 'SuperAdminGroup' in groups or 'AdminGroup' in groups:
            return Notification.objects.filter(processed=False)
        else:
            return Notification.objects.filter(processed=False, target=self.request.user)


class NotificationCreate(CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'create_project.html'
    success_url = reverse_lazy('management.notifications')

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(NotificationCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['creator'] = self.request.user
        print initial
        return initial


class NotificationUpdate(UpdateView):
    model = Notification
    template_name = 'create_project.html'
    success_url = reverse_lazy('management.notifications')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NotificationUpdate, self).get_context_data(**kwargs)
        # Add extra context variable
        context['title'] = _('Modify Notification')
        return context


class NotificationDelete(DeleteView):
    model = Notification
    template_name = 'gateway_confirm_delete.html'
    success_url = reverse_lazy('management.notifications')


class NotificationDetail(DetailView):
    model = Notification
    template_name = 'notification_detail.html'


def notification_data(request):
    groups = request.user.groups.values_list('name', flat=True)
    if 'SuperAdminGroup' in groups or 'AdminGroup' in groups:
        query_set = Notification.objects.filter(processed=False).order_by('-date')
    else:
        query_set = Notification.objects.filter(processed=False, target=request.user).order_by('-date')
    data = serializers.serialize("json", query_set)
    print data

    return HttpResponse(data, content_type="application/json")
