from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Course
from .forms import AppUserCreationForm


class SignUpView(CreateView):
    form_class = AppUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


def homeView(request):
    if not request.user.is_authenticated:
        return render(request, 'landing.html')

    if request.user.is_instructor:
        instructor_courses_list = Course.objects.filter(instructor=request.user)

        page = request.GET.get('page', 1)
        paginator = Paginator(instructor_courses_list, 5)
        try:
            instructor_courses = paginator.page(page)
        except PageNotAnInteger:
            instructor_courses = paginator.page(1)
        except EmptyPage:
            instructor_courses = paginator.page(paginator.num_pages)

        return render(request, 'users/instructorhome.html', {'instructor_courses': instructor_courses, })

    student_courses_list = Course.objects.filter(students=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(student_courses_list, 5)
    try:
        student_courses = paginator.page(page)
    except PageNotAnInteger:
        student_courses = paginator.page(1)
    except EmptyPage:
        student_courses = paginator.page(paginator.num_pages)
    return render(request, 'users/studenthome.html', {'student_courses': student_courses, })
