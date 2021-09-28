from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from courses.models import Course
from .forms import AppUserCreationForm


class SignUpView(CreateView):
    form_class = AppUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


def homeView(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    if request.user.is_instructor:
        instructor_courses = Course.objects.filter(instructor=request.user)
        return render(request, 'users/instructorhome.html', {'instructor_courses': instructor_courses, })
    student_courses = Course.objects.filter(students=request.user)
    return render(request, 'users/studenthome.html', {'student_courses': student_courses, })
