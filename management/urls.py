from django.conf.urls import patterns, include, url
import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    #Notification
    url(r'^notifications', login_required(views.NotificationList.as_view()), name='management.notifications'),
    url(r'^notification/data/$', login_required(views.notification_data), name='management.notification_data'),
    url(r'^notification/add/$', login_required(views.NotificationCreate.as_view()), name='management.notification.add'),
    url(r'^notification/(?P<pk>\d+)/$', login_required(views.NotificationUpdate.as_view()), name='management.notification.update'),
    url(r'^notification/(?P<pk>\d+)/delete/$', login_required(views.NotificationDelete.as_view()), name='management.notification.delete'),
    url(r'^notification/(?P<pk>\d+)/detail/$', login_required(views.NotificationDetail.as_view()), name='management.notification.detail'),

    #gateway
    url(r'^gateways', login_required(views.GatewayList.as_view()), name='management.gateways'),
    url(r'^gateway/add/$', login_required(views.GatewayCreate.as_view()), name='management.gateway.add'),
    url(r'^gateway/(?P<pk>\d+)/$', login_required(views.GatewayUpdate.as_view()), name='management.gateway.update'),
    url(r'^gateway/(?P<pk>\d+)/delete/$', login_required(views.GatewayDelete.as_view()), name='management.gateway.delete'),

    #wifi client
    url(r'^clients', login_required(views.WifiClientList.as_view()), name='management.clients'),

    #AD Statistics
    url(r'^adstats', login_required(views.AdStatsList.as_view()), name='management.adstats'),

    #AD
    url(r'^ads', login_required(views.AdList.as_view()), name='management.ads'),
    url(r'^ad/add/$', login_required(views.AdCreate.as_view()), name='management.ad.add'),
    url(r'^ad/(?P<pk>\d+)/$', login_required(views.AdUpdate.as_view()), name='management.ad.update'),
    url(r'^ad/(?P<pk>\d+)/delete/$', login_required(views.AdDelete.as_view()), name='management.ad.delete'),
    url(r'^ad/(?P<pk>\d+)/detail/$', login_required(views.AdDetail.as_view()), name='management.ad.detail'),

    #SMS Template
    url(r'^templates', login_required(views.SmsTemplateList.as_view()), name='management.templates'),
    url(r'^template/add/$', login_required(views.SmsTemplateCreate.as_view()), name='management.template.add'),
    url(r'^template/(?P<pk>\d+)/$', login_required(views.SmsTemplateUpdate.as_view()), name='management.template.update'),
    url(r'^template/(?P<pk>\d+)/delete/$', login_required(views.SmsTemplateDelete.as_view()), name='management.template.delete'),

)


