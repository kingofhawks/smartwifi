from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    url(r'^login_ad', views.login_ad, name='login_ad'),
    url(r'^login', views.login, name='login'),
    url(r'^auth', views.auth, name='auth'),
    url(r'^portal', views.portal, name='portal'),
    url(r'^ping', views.ping, name='ping'),


)


