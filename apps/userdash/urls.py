from django.conf.urls import url
from . import views
urlpatterns  = [
    url(r'^login$', views.login),
    url(r'^userlogin$', views.userlogin),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^profile$', views.profile),
    url(r'^wall/(?P<id>\d)$', views.wall),
    url(r'^message$', views.message),
    url(r'^comment$', views.comment),
    url(r'^updateprofile$', views.updateprofile),
    url(r'^selfregister$', views.selfregister),
    url(r'^adminusercreate$', views.adminusercreate),
    url(r'^edit/(?P<id>\d)$', views.edit),
    url(r'^updateinfo$', views.updateinfo),
    url(r'^newuser$', views.newuser),
    url(r'^destroy/(?P<id>\d)$', views.destroy),
    url(r'^$', views.index),
]