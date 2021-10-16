from django.contrib import admin

from assignments.models import Assignment, Question, AssignmentSubmission, QuestionSubmission
from courses.admin import AssignmentInline


class QuestionSubmissionInline(admin.TabularInline):
    model = QuestionSubmission


class AssignmentSubmissionAdmin(admin.ModelAdmin):
    model = AssignmentSubmission
    inlines = (QuestionSubmissionInline,)


admin.site.register(AssignmentSubmission, AssignmentSubmissionAdmin)
admin.site.register(QuestionSubmission)
