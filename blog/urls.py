# -*- coding: utf-8 -*-
# @Time    : 2020/5/7 19:50
# @Author  : lucky dog
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tag/<int:pk>', views.tag, name='tag'),
    path('search/', views.search, name='search'),
    path('about', views.about, name='about'),
    path('timeline', views.timeline, name='timeline'),
    path('contact', views.contact, name='contact'),
]