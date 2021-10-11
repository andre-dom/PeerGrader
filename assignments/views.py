from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from assignments.models import Assignment, Question
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


class PublishAssignment(UpdateView):
    model = Assignment
    template_name = 'assignments/publish_assignment.html'
    fields = ('is_published',)
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = "/"


class CreateQuestion(CreateView):
    model = Question
    template_name = 'questions/createquestion.html'
    fields = ('question_body', 'point_value',)
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        form.instance.index = Assignment.objects.get(slug=self.kwargs['assignment_slug']).numQuestions() + 1
        return super(CreateQuestion, self).form_valid(form)


class EditQuestion(UpdateView):
    model = Question
    template_name = 'questions/editquestion.html'
    fields = ('question_body', 'point_value',)
    slug_url_kwarg = 'index'
    slug_field = 'index'
    success_url = "/"

    def get_queryset(self):
        assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        return Question.objects.filter(assignment=assignment, index=self.kwargs['index'])


class DeleteQuestion(DeleteView):
    model = Question
    slug_url_kwarg = 'index'
    slug_field = 'index'
    success_url = "/"
    template_name = 'questions/deletequestion.html'

    def get_queryset(self):
        assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        return Question.objects.filter(assignment=assignment, index=self.kwargs['index'])


assignment_detail_view = login_required(AssignmentView.as_view())
assignment_create_view = login_required(CreateAssignment.as_view())
assignment_delete_view = login_required(DeleteAssignment.as_view())
assignment_publish_view = login_required(PublishAssignment.as_view())
question_edit_view = login_required(EditQuestion.as_view())
question_create_view = login_required(CreateQuestion.as_view())
question_delete_view = login_required(DeleteQuestion.as_view())
