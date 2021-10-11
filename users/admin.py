from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# allow us to access custom user model from admin panel
from django.contrib.auth.hashers import make_password

from .forms import AppUserCreationForm, AppUserChangeForm
from .models import AppUser

from import_export import resources
from import_export.admin import ImportExportModelAdmin


# class AppUserAdmin(UserAdmin):
#     add_form = AppUserCreationForm
#     form = AppUserChangeForm
#     model = AppUser
#     list_display = ['username', 'is_instructor']
#     fieldsets = UserAdmin.fieldsets + (
#             (None, {'fields': ('is_instructor',)}),
#     )


class AppUserResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        value = row['password']
        row['password'] = make_password(value)

    class Meta:
        model = AppUser
        import_id_fields = ('username',)
        fields = ('username', 'password', 'is_instructor')


class AppUserAdmin(ImportExportModelAdmin):
    resource_class = AppUserResource


admin.site.register(AppUser, AppUserAdmin)
