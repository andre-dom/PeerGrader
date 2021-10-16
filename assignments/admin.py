from django.contrib import admin

from assignments.models import Assignment, Question, AssignmentSubmission, QuestionSubmission
from courses.admin import AssignmentInline


# class QuestionInline(admin.TabularInline):
#     model = Question
#     # readonly_fields = ('created_at', 'slug')
#     list_display = ('question_body', 'point_value',)
#
#
# class AssignmentAdmin(admin.ModelAdmin):
#     # add_form = AppUserCreationForm
#     # form = AppUserChangeForm
#     model = Assignment
#     readonly_fields = ('slug',)
#     list_display = ('name',)
#     inlines = (QuestionInline,)
#     # filter_horizontal = ('students',)
#
#     # fieldsets = UserAdmin.fieldsets + (
#     #         (None, {'fields': ('is_instructor',)}),
#     # )
#
#
# admin.site.register(Assignment, AssignmentAdmin)
# admin.site.register(Question)

class QuestionSubmissionInline(admin.TabularInline):
    model = QuestionSubmission
    # readonly_fields = ('created_at', 'slug')
    # list_display = ('question_body', 'point_value',)


class AssignmentSubmissionAdmin(admin.ModelAdmin):
    # add_form = AppUserCreationForm
    # form = AppUserChangeForm
    model = AssignmentSubmission
    inlines = (QuestionSubmissionInline,)
    # readonly_fields = ('slug',)
    # list_display = ('name',)
    # filter_horizontal = ('students',)

    # fieldsets = UserAdmin.fieldsets + (
    #         (None, {'fields': ('is_instructor',)}),
    # )


admin.site.register(AssignmentSubmission, AssignmentSubmissionAdmin)
admin.site.register(QuestionSubmission)
