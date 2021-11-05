from django.contrib import admin

# Register your models here.

from .models import Course
from assignments.models import Assignment

import nested_admin

from assignments.models import Assignment, Question


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    # readonly_fields = ('created_at', 'slug')
    list_display = ('question_body', 'point_value',)


class AssignmentAdmin(nested_admin.NestedModelAdmin):
    # add_form = AppUserCreationForm
    # form = AppUserChangeForm

    model = Assignment
    readonly_fields = ('name',)
    list_display = ('course',)
    inlines = (QuestionInline,)


class AssignmentInline(nested_admin.NestedTabularInline):
    model = Assignment
    readonly_fields = ('created_at', 'slug')
    list_display = ('name', 'course', 'due_date')
    inlines = (QuestionInline,)


class CourseAdmin(nested_admin.NestedModelAdmin):
    # add_form = AppUserCreationForm
    # form = AppUserChangeForm
    model = Course
    readonly_fields = ('slug',)
    list_display = ('name', 'instructor',)
    inlines = (AssignmentInline,)
    filter_horizontal = ('students',)

    # fieldsets = UserAdmin.fieldsets + (
    #         (None, {'fields': ('is_instructor',)}),
    # )


admin.site.register(Course, CourseAdmin)
admin.site.register(Question)
admin.site.register(Assignment)