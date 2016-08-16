from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^login/user$', views.login),
    url(r'^register$', views.register),
    url(r'^create/user$', views.create),
    url(r'^dashboard/admin$', views.showadmin),
    ]
