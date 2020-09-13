"""Needle app: Forms tags template tag."""
# -*- coding: utf-8 -*-

from django import template
from django.forms import CheckboxInput, RadioSelect, Textarea, Select, FileInput
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)


@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.filter(name='is_file')
def is_file(field):
    return field.field.widget.__class__.__name__ == FileInput().__class__.__name__


@register.filter(name='is_select')
def is_select(field):
    return field.field.widget.__class__.__name__ == Select().__class__.__name__


@register.filter(name='is_text_area')
def is_text_area(field):
    return field.field.widget.__class__.__name__ == Textarea().__class__.__name__


@register.filter(name='is_radio_select')
def is_radio_select(field):
    return field.field.widget.__class__.__name__ == RadioSelect().__class__.__name__


@register.filter(name='cool_number')
def cool_number(value, num_decimals=2):
    """
        Django template filter to convert regular numbers to a
        cool format (ie: 2K, 434.4K, 33M...)
        :param value: number
        :param num_decimals: Number of decimal digits
    """
    int_value = int(value)
    formatted_number = '{{:.{}f}}'.format(num_decimals)
    if int_value < 1000:
        return str(int_value)
    elif int_value < 1000000:
        return formatted_number.format(int_value / 1000.0).rstrip('0.') + 'K'
    else:
        return formatted_number.format(int_value / 1000000.0).rstrip('0.') + 'M'
