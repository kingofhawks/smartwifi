from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    url(r'^login', views.login, name='api.login'),
    url(r'^auth', views.auth, name='api.auth'),
    url(r'^portal', views.portal, name='api.portal'),
    url(r'^ping', views.ping, name='api.ping'),


)


