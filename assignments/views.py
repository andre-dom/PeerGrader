from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView

from assignments.models import Assignment
from courses.models import Course


class AssignmentView(DetailView):
    model = Assignment
    template_name = 'assignments/assignmentview.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'


class CreateAssignment(CreateView):
    model = Assignment
    template_name = 'assignments/createassignment.html'
    fields = ('name', 'due_date',)

    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.course = Course.objects.get(slug=self.kwargs['course_slug'])
        return super(CreateAssignment, self).form_valid(form)


class DeleteAssignment(DeleteView):
    model = Assignment
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = "/"
    template_name = 'assignments/deleteassignment.html'


assignment_detail_view = login_required(AssignmentView.as_view())
assignment_create_view = login_required(CreateAssignment.as_view())
assignment_delete_view = login_required(DeleteAssignment.as_view())
