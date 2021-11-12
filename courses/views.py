from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Course


@login_required()
def course_view(request, slug):
    course = Course.objects.get(slug=slug)
    user = request.user

    # Make sure authenticated user is part of the course
    if not (course.instructor == user or (user in course.students.all())):
        return redirect('/')

    # dont show unpublished assignments to students
    if user.is_instructor:
        assignment_list = course.assignments.all().order_by('slug')
    else:
        assignment_list = course.assignments.filter(~Q(state="unpublished")).order_by('slug')

    page = request.GET.get('page', 1)
    paginator = Paginator(assignment_list, 5)
    try:
        assignments = paginator.page(page)
    except PageNotAnInteger:
        assignments = paginator.page(1)
    except EmptyPage:
        assignments = paginator.page(paginator.num_pages)

    if request.user.is_instructor:
        return render(request, 'courses/instructorcourseview.html', {'course': course, 'assignments': assignments, })
    else:
        return render(request, 'courses/studentcourseview.html', {'course': course, 'assignments': assignments, })


course_detail_view = login_required(course_view)
