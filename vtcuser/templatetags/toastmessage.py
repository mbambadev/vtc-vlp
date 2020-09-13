"""Custom toast message templetag."""
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django import template

register = template.Library()


@register.inclusion_tag('includes/toast_message.html')
def toast_message(text, color_name="bg-blue"):
    """Template tag for displaying notification messages."""

    context = dict()
    context['text'] = text
    context['color_name'] = color_name
    return context
