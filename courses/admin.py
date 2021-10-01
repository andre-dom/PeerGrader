from django.contrib import admin

# Register your models here.
from .models import Course
from assignments.models import Assignment


class AssignmentInline(admin.TabularInline):
    model = Assignment
    readonly_fields = ('created_at', 'slug')
    list_display = ('name', 'course', 'due_date')


class CourseAdmin(admin.ModelAdmin):
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
admin.site.register(Assignment)
