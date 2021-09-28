from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.detail import DetailView

from courses.models import Course


class CourseView(DetailView):
    model = Course
    template_name = 'courses/courseview.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'


course_detail_view = login_required(CourseView.as_view())
