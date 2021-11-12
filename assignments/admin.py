from django.contrib import admin

from assignments.models import Assignment, Question, AssignmentSubmission, QuestionSubmission, GradedQuestionSubmission, \
    GradedAssignmentSubmission
from courses.admin import AssignmentInline


class QuestionSubmissionInline(admin.TabularInline):
    model = QuestionSubmission


class AssignmentSubmissionAdmin(admin.ModelAdmin):
    model = AssignmentSubmission
    inlines = (QuestionSubmissionInline,)


class GradedQuestionSubmissionInline(admin.TabularInline):
    model = GradedQuestionSubmission


class GradedAssignmentSubmissionAdmin(admin.ModelAdmin):
    model = GradedAssignmentSubmission
    inlines = (GradedQuestionSubmissionInline,)


admin.site.register(AssignmentSubmission, AssignmentSubmissionAdmin)
admin.site.register(QuestionSubmission)

admin.site.register(GradedAssignmentSubmission, GradedAssignmentSubmissionAdmin)
admin.site.register(GradedQuestionSubmission)
