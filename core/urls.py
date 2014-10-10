from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'worksmart.views.home', name='home'),
    #url(r'^$', views.trend, name='trend'),
    url(r'^dashboard/$', views.dashboard, name='core.dashboard'),
)
