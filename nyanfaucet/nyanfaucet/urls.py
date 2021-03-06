﻿"""nyanfaucet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from web import views

urlpatterns = [
  url(r'^admin/', include(admin.site.urls)),
  
  url(r'^/?$', views.DefaultView.as_view(), name='default'),
  
  url(r'^login$', views.LoginView.as_view(), name='login'),
  url(r'^register$', views.RegisterView.as_view(), name='register'),
  url(r'^logout$', views.LogoutView.as_view(), name='logout'),
  url(r'^activator/(?P<nonce>\w+)?$', views.ActivationHelper.as_view(), name='activation_helper'),

  url(r'^donate$', views.DonateView.as_view(), name='donate'),
  url(r'^play$', views.PlayView.as_view(), name='play'),
  url(r'^withdraw$', views.WithdrawView.as_view(), name='withdraw'),
  url(r'^history', views.HistoryView.as_view(), name='account'),
  
]
