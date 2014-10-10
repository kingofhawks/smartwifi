from django.utils.translation import ugettext as _
from django import template
from management.models import Selection, NOTIFICATION_TYPE_CHOICES, Project
from django.shortcuts import get_object_or_404
register = template.Library()

@register.filter(name='approve_state')
def approve_state(value):
    if value:
        return _('Approved')
    else:
        return _('Deny')


@register.filter(name='vote_state')
def vote_state(value, arg):
    print arg
    if value:
        return _('Thumbs Up')
    elif arg is None:
        return _('Not yet voted')
    else:
        return _('Thumbs Down')

@register.filter(name='vote_result')
def vote_result(value):
    status = _('Not yet voted')
    total = Selection.objects.filter(project_id=value).count()
    project = get_object_or_404(Project, pk=value)
    up_ratio = 0

    from datetime import datetime
    from django.utils import timezone

    if project.finish_vote_date is None:
        return status
    elif project.finish_vote_date > timezone.make_aware(datetime.now(), timezone.get_default_timezone()):
        status = _('Vote is going on')
    elif total == 0:
        return status
    else:
        passed_count = Selection.objects.filter(project_id=value, passed=True).count()
        up_ratio = passed_count*1.0/total

        print '{}:{}:{}'.format(passed_count, total, up_ratio)

        if up_ratio >= 2*1.0/3:
            status = _('Thumbs Up')
        elif up_ratio > 0:
            status = _('Thumbs Down')

    return status


@register.filter(name='notification_type')
def notification_type(value):
    for choice in NOTIFICATION_TYPE_CHOICES:
        if choice[0] == value:
            return choice[1];
    return ''
