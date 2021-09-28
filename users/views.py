from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import AppUserCreationForm


class SignUpView(CreateView):
    form_class = AppUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


def homeView(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    if request.user.is_instructor:
        return render(request, 'users/instructorhome.html')
    return render(request, 'users/studenthome.html')
