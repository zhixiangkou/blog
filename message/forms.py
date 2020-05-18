# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 18:14
# @Author  : lucky dog

from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'message']
