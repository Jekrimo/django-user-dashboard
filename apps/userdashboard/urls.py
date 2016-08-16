from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^login/user$', views.login),
    url(r'^register$', views.register),
    url(r'^create/user$', views.create),
    url(r'^dashboard/user$', views.show),
    url(r'^dashboard/admin$', views.showadmin),
    url(r'^users/show/(?P<id>\d+)$', views.showusers),
    url(r'^clear$', views.signout),
    url(r'^destroy/(?P<id>\d+)$', views.delete),
    url(r'^users/edit/(?P<id>\d+)$', views.edit),
    url(r'^users/edit/(?P<id>\d+)/update$', views.update),
    url(r'^users/edit/(?P<id>\d+)/update/pass$', views.updatepass),
    url(r'^users/new$', views.new),
    url(r'^create/new$', views.createnew),
    ]
