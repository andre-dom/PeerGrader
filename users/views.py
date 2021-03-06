from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Course
from .forms import AppUserCreationForm
from .models import AppUser


class SignUpView(CreateView):
    form_class = AppUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


class EditUsername(UpdateView):
    model = AppUser
    success_url = reverse_lazy('home')
    template_name = 'registration/changeusername.html'
    fields = ('username',)

    def get_object(self):  # override how to look for object, user has no slug so have to use get_object
        return self.request.user


def home_view(request):
    if not request.user.is_authenticated:
        return render(request, 'landing.html')

    if request.user.is_instructor:
        instructor_courses_list = Course.objects.filter(instructor=request.user).order_by('slug')

        page = request.GET.get('page', 1)
        paginator = Paginator(instructor_courses_list, 5)
        try:
            instructor_courses = paginator.page(page)
        except PageNotAnInteger:
            instructor_courses = paginator.page(1)
        except EmptyPage:
            instructor_courses = paginator.page(paginator.num_pages)

        return render(request, 'users/instructorhome.html', {'instructor_courses': instructor_courses, })

    student_courses_list = Course.objects.filter(students=request.user).order_by('slug')
    page = request.GET.get('page', 1)
    paginator = Paginator(student_courses_list, 5)
    try:
        student_courses = paginator.page(page)
    except PageNotAnInteger:
        student_courses = paginator.page(1)
    except EmptyPage:
        student_courses = paginator.page(paginator.num_pages)
    return render(request, 'users/studenthome.html', {'student_courses': student_courses, })
