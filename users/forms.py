# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AppUser


class AppUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = AppUser
        fields = ('username',)


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = AppUser
        fields = ('username',)
