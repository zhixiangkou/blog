# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 18:10
# @Author  : lucky dog

from django.urls import path

from . import views

app_name = 'message'
urlpatterns = [
    path('message', views.message, name='message'),
]