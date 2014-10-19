from django.forms import ModelForm, Textarea, DateTimeField
from models import (Notification)


class NotificationForm(ModelForm):

    class Meta:
        model = Notification
        widgets = {
            'content': Textarea,
        }
        exclude = ['processed']