from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from assignments.models import Assignment


class AssignmentView(DetailView):
    model = Assignment
    template_name = 'assignments/assignmentview.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'


assignment_detail_view = login_required(AssignmentView.as_view())

