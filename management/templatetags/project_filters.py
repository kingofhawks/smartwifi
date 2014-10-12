from django.utils.translation import ugettext as _
from django import template
from django.shortcuts import get_object_or_404
register = template.Library()

#@register.filter(name='approve_state')
#def approve_state(value):
#    if value:
#        return _('Approved')
#    else:
#        return _('Deny')
#
#
#@register.filter(name='vote_state')
#def vote_state(value, arg):
#    print arg
#    if value:
#        return _('Thumbs Up')
#    elif arg is None:
#        return _('Not yet voted')
#    else:
#        return _('Thumbs Down')

