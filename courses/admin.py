from django.contrib import admin

# Register your models here.
from .models import Course


class CourseAdmin(admin.ModelAdmin):
    # add_form = AppUserCreationForm
    # form = AppUserChangeForm
    model = Course
    # list_display = ['name', ]
    # fieldsets = UserAdmin.fieldsets + (
    #         (None, {'fields': ('is_instructor',)}),
    # )


admin.site.register(Course)
