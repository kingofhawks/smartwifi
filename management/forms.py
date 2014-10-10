from django.forms import ModelForm, Textarea, DateTimeField
from models import (Project, Submission, ApplicationReview, ElementEvaluationForm, BatchEvaluationForm, StageEvaluationForm,
                    UnitEvaluationForm, Notification)


#Create form from models
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        #fields = ['name', 'description', 'location', 'area', 'cost', 'structure_type', 'start_date', 'end_date',
        #          'construct_company', 'postal_address', 'zipcode']
        #exclude = ['user']


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        exclude = ['date']


class ReviewForm(ModelForm):
    class Meta:
        model = ApplicationReview
        exclude = ['date']


class ElementEvaluationFormForm(ModelForm):
    class Meta:
        model = ElementEvaluationForm
        exclude = ['date']


class BatchEvaluationFormForm(ModelForm):
    class Meta:
        model = BatchEvaluationForm
        exclude = ['date']


class StageEvaluationFormForm(ModelForm):
    class Meta:
        model = StageEvaluationForm
        exclude = ['date']


class UnitEvaluationFormForm(ModelForm):
    class Meta:
        model = UnitEvaluationForm
        exclude = ['date']


class NotificationForm(ModelForm):


    class Meta:
        model = Notification
        widgets = {
            'content': Textarea,
        }