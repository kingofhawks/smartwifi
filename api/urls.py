from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    url(r'^login', views.login, name='api.login'),
    url(r'^auth', views.login, name='api.auth'),
    url(r'^portal', views.login, name='api.portal'),
    url(r'^ping', views.login, name='api.ping'),


)


