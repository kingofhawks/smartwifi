from django.utils.translation import ugettext as _
from django import template
from django.shortcuts import get_object_or_404
register = template.Library()

@register.filter(name='yes_no')
def yes_no(value):
    if value:
        return _('Yes')
    else:
        return _('No')

@register.filter(name='notification_target')
def notification_target(value):
    if value is None:
        return _('All')
    else:
        return value

