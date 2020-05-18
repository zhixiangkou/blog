# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 20:40
# @Author  : lucky dog

from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
    path('comment/<int:post_pk>', views.comment, name='comment'),
]