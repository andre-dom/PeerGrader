from django.contrib import admin

from assignments.models import Assignment, Question
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
