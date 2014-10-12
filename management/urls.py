from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    #Notification
    url(r'^notifications', views.NotificationList.as_view(), name='management.notifications'),
    url(r'^notification/data/$', views.notification_data, name='management.notification_data'),
    url(r'^notification/add/$', views.NotificationCreate.as_view(), name='management.notification.add'),
    url(r'^notification/(?P<pk>\d+)/$', views.NotificationUpdate.as_view(), name='management.notification.update'),
    url(r'^notification/(?P<pk>\d+)/delete/$', views.NotificationDelete.as_view(), name='management.notification.delete'),

    #gateway
    url(r'^gateways', views.GatewayList.as_view(), name='management.gateways'),
    url(r'^gateway/add/$', views.GatewayCreate.as_view(), name='management.gateway.add'),
    url(r'^gateway/(?P<pk>\d+)/$', views.GatewayUpdate.as_view(), name='management.gateway.update'),
    url(r'^gateway/(?P<pk>\d+)/delete/$', views.GatewayDelete.as_view(), name='management.gateway.delete'),

    #wifi client
    url(r'^clients', views.WifiClientList.as_view(), name='management.clients'),

    #AD Statistics
    url(r'^adstats', views.AdStatsList.as_view(), name='management.adstats'),

    #AD
    url(r'^ads', views.AdList.as_view(), name='management.ads'),
    url(r'^ad/add/$', views.AdCreate.as_view(), name='management.ad.add'),
    url(r'^ad/(?P<pk>\d+)/$', views.AdUpdate.as_view(), name='management.ad.update'),
    url(r'^ad/(?P<pk>\d+)/delete/$', views.AdDelete.as_view(), name='management.ad.delete'),
    url(r'^ad/(?P<pk>\d+)/detail/$', views.AdDetail.as_view(), name='management.ad.detail'),

    #SMS Template
    url(r'^templates', views.SmsTemplateList.as_view(), name='management.templates'),
    url(r'^template/add/$', views.SmsTemplateCreate.as_view(), name='management.template.add'),
    url(r'^template/(?P<pk>\d+)/$', views.SmsTemplateUpdate.as_view(), name='management.template.update'),
    url(r'^template/(?P<pk>\d+)/delete/$', views.SmsTemplateDelete.as_view(), name='management.template.delete'),

)


