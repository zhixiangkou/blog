# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 19:23
# @Author  : lucky dog

from django import template
from ..forms import MessageForm

register = template.Library()


@register.inclusion_tag('message/inclusions/_form.html', takes_context=True)
def show_message_form(context, form=None):
    if form is None:
        form = MessageForm()
    return {
        'form': form,
    }

