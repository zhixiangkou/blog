# -*- coding: utf-8 -*-
# @Time    : 2020/5/9 20:01
# @Author  : lucky dog


from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
