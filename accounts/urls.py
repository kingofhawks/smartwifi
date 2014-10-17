from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^reset/$', views.password_reset, name='reset'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^captcha/$', views.refresh_captcha, name='accounts.captcha'),
    url(r'^companies/$', views.CompanyList.as_view(), name='accounts.companies'),

    #SysAdmin
    url(r'^sysadmins', views.SysAdminList.as_view(), name='accounts.sysadmins'),
    url(r'^sysadmin/add/$', views.SysAdminCreate.as_view(), name='accounts.sysadmin.add'),
    url(r'^sysadmin/(?P<pk>\d+)/$', views.SysAdminUpdate.as_view(), name='accounts.sysadmin.update'),
    url(r'^sysadmin/(?P<pk>\d+)/delete/$', views.SysAdminDelete.as_view(), name='accounts.sysadmin.delete'),

    #Agent
    url(r'^agents', views.AgentList.as_view(), name='accounts.agents'),
    url(r'^agent/add/$', views.AgentCreate.as_view(), name='accounts.agent.add'),
    url(r'^agent/(?P<pk>\d+)/$', views.AgentUpdate.as_view(), name='accounts.agent.update'),
    url(r'^agent/(?P<pk>\d+)/delete/$', views.AgentDelete.as_view(), name='accounts.agent.delete'),

    #Customer
    url(r'^customers', views.CustomerList.as_view(), name='accounts.customers'),
    url(r'^customer/add/$', views.CustomerCreate.as_view(), name='accounts.customer.add'),
    url(r'^customer/(?P<pk>\d+)/$', views.CustomerUpdate.as_view(), name='accounts.customer.update'),
    url(r'^customer/(?P<pk>\d+)/delete/$', views.CustomerDelete.as_view(), name='accounts.customer.delete'),
)
