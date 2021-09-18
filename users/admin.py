from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# allow us to access custom user model from admin panel
from .forms import AppUserCreationForm, AppUserChangeForm
from .models import AppUser


class AppUserAdmin(UserAdmin):
    add_form = AppUserCreationForm
    form = AppUserChangeForm
    model = AppUser
    list_display = ['username', 'is_instructor']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('is_instructor',)}),
    ) #this will allow to change these fields in admin module


admin.site.register(AppUser, AppUserAdmin)