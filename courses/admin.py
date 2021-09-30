from django.contrib import admin

# Register your models here.
from .models import Course


class CourseAdmin(admin.ModelAdmin):
    # add_form = AppUserCreationForm
    # form = AppUserChangeForm
    model = Course
    readonly_fields = ('slug',)
    list_display = ('name', 'instructor')
    filter_horizontal = ('students',)
    # fieldsets = UserAdmin.fieldsets + (
    #         (None, {'fields': ('is_instructor',)}),
    # )


admin.site.register(Course, CourseAdmin)
