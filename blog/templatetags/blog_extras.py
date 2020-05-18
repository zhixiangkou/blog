# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 18:10
# @Author  : lucky dog

from django import template
from django.db.models import Count

from ..models import Post, Category, Tag, Profile

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }


@register.inclusion_tag('blog/inclusions/_profile1.html', takes_context=True)
def show_profile1(context):
    profile1_list = Profile.objects.all()
    return {
        'profile1_list': profile1_list,
    }


@register.inclusion_tag('blog/inclusions/_profile2.html', takes_context=True)
def show_profile2(context):
    profile2_list = Profile.objects.all()
    return {
        'profile2_list': profile2_list,
    }


@register.inclusion_tag('blog/inclusions/_profile3.html', takes_context=True)
def show_profile3(context):
    profile3_list = Profile.objects.all()
    return {
        'profile3_list': profile3_list,
    }