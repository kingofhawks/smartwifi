from django.contrib import admin
from models import (Notification, Gateway, WifiClient, Ad, AdStat)
from django.utils.translation import ugettext as _


class SubmissionAdmin(admin.ModelAdmin):
    fieldsets = [('Project Info', {'fields':['project', 'grade']}),
                 ('Company Info', {'fields':['person_in_charge','phone1','technical_in_charge','phone2','company_technical_in_charge','phone3']}),
                 (None,{'fields':['content','measures', 'schedule','benefits', 'company_opinion', 'management_opinion','approved',  'date']})]
    list_display = ('project', 'grade','date')
    actions = ['change_grade']

    def change_grade(self, request, queryset):
        rows_updated = queryset.update(grade=1)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
    change_grade.short_description = _("Change Grade")


#admin.site.register(Submission, SubmissionAdmin)
#admin.site.register(Project)
#admin.site.register(ApplicationReview)
#admin.site.register(SelfEvaluation)
#admin.site.register(Selection)
#admin.site.register(PM10)
#admin.site.register(ProgressMonitor)
#admin.site.register(Picture)
#admin.site.register(ControlItem)
#admin.site.register(GeneralItem)
#admin.site.register(ExcellentItem)
#admin.site.register(ElementEvaluationForm)
#admin.site.register(BatchEvaluationForm)
#admin.site.register(StageEvaluationForm)
#admin.site.register(UnitEvaluationForm)

admin.site.register(Notification)
admin.site.register(Gateway)
admin.site.register(WifiClient)
admin.site.register(Ad)
admin.site.register(AdStat)

