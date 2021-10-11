from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Course


@login_required()
def course_view(request, slug):
    course = Course.objects.get(slug=slug)
    assignment_list = course.assignments.values()

    page = request.GET.get('page', 1)
    paginator = Paginator(assignment_list, 5)
    try:
        assignments = paginator.page(page)
    except PageNotAnInteger:
        assignments = paginator.page(1)
    except EmptyPage:
        assignments = paginator.page(paginator.num_pages)

    return render(request, 'courses/courseview.html', {'course': course, 'assignments': assignments, })


course_detail_view = login_required(course_view)
