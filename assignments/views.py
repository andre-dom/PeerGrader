from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from assignments.models import Assignment, Question, AssignmentSubmission
from courses.models import Course

from django import forms


class AssignmentView(DetailView):
    model = Assignment
    template_name = 'assignments/assignmentview.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

    def dispatch(self, request, *args, **kwargs):
        # validate user
        assignment = Assignment.objects.get(slug=self.kwargs['slug'])
        course = assignment.course
        user = request.user
        if not (course.instructor == user or (user in course.students.all())):
            return redirect('/')
        else:
            return super(AssignmentView, self).dispatch(request, *args, **kwargs)


class CreateAssignment(CreateView):
    model = Assignment
    template_name = 'assignments/createassignment.html'
    fields = ('name', 'due_date',)

    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.course = Course.objects.get(slug=self.kwargs['course_slug'])
        return super(CreateAssignment, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # validate user
        course = Course.objects.get(slug=self.kwargs['course_slug'])
        user = request.user
        if not (course.instructor == user):
            return redirect('/')
        else:
            return super(CreateAssignment, self).dispatch(request, *args, **kwargs)


class DeleteAssignment(DeleteView):
    model = Assignment
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = "/"
    template_name = 'assignments/deleteassignment.html'

    def dispatch(self, request, *args, **kwargs):
        # validate user
        assignment = Assignment.objects.get(slug=self.kwargs['slug'])
        course = assignment.course
        user = request.user
        if not (course.instructor == user):
            return redirect('/')
        else:
            return super(DeleteAssignment, self).dispatch(request, *args, **kwargs)


class EditAssignment(UpdateView):
    model = Assignment
    slug_url_kwarg = 'slug' #use slug to get specific assignment
    slug_field = 'slug'
    success_url = "/" #sending to home page
    template_name = 'assignments/editassignment.html'
    fields = ('name', 'due_date',) #specifying what variables in the model need to be modified


class PublishAssignment(UpdateView):
    model = Assignment
    template_name = 'assignments/publish_assignment.html'
    fields = ('is_published',)
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = "/"

    def clean(self):
        assignment = Assignment.objects.get(slug=self.kwargs['slug'])
        if assignment.questions.get_values().len() == 0:
            raise forms.ValidationError("No questions in assignment")

    def dispatch(self, request, *args, **kwargs):
        # validate user
        assignment = Assignment.objects.get(slug=self.kwargs['slug'])
        course = assignment.course
        user = request.user
        if not (course.instructor == user):
            return redirect('/')
        else:
            return super(PublishAssignment, self).dispatch(request, *args, **kwargs)


class CreateQuestion(CreateView):
    model = Question
    template_name = 'questions/createquestion.html'
    fields = ('question_body', 'point_value',)
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        form.instance.index = Assignment.objects.get(slug=self.kwargs['assignment_slug']).numQuestions() + 1
        return super(CreateQuestion, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # validate user
        assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        course = assignment.course
        user = request.user
        if not (course.instructor == user):
            return redirect('/')
        else:
            return super(CreateQuestion, self).dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        # validate user
        assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        course = assignment.course
        user = request.user
        if not (course.instructor == user):
            return redirect('/')
        else:
            return super(EditQuestion, self).dispatch(request, *args, **kwargs)


class DeleteQuestion(DeleteView):
    model = Question
    slug_url_kwarg = 'index'
    slug_field = 'index'
    success_url = "/"
    template_name = 'questions/deletequestion.html'

    def get_queryset(self):
        assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        return Question.objects.filter(assignment=assignment, index=self.kwargs['index'])

    def dispatch(self, request, *args, **kwargs):
        # validate user
        assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        course = assignment.course
        user = request.user
        if not (course.instructor == user):
            return redirect('/')
        else:
            return super(DeleteQuestion, self).dispatch(request, *args, **kwargs)


class CreateSubmission(CreateView):
    model = AssignmentSubmission
    template_name = 'submissions/create_submission.html'
    fields = ('is_submitted',)

    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        return super(CreateSubmission, self).form_valid(form)

    # def dispatch(self, request, *args, **kwargs):
    #     # validate user
    #     course = Course.objects.get(slug=self.kwargs['course_slug'])
    #     user = request.user
    #     if not (course.instructor == user):
    #         return redirect('/')
    #     else:
    #         return super(CreateSubmission, self).dispatch(request, *args, **kwargs)


assignment_detail_view = login_required(AssignmentView.as_view())
assignment_create_view = login_required(CreateAssignment.as_view())
assignment_delete_view = login_required(DeleteAssignment.as_view())
assignment_publish_view = login_required(PublishAssignment.as_view())
assignment_edit_view = login_required(EditAssignment.as_view())

question_edit_view = login_required(EditQuestion.as_view())
question_create_view = login_required(CreateQuestion.as_view())
question_delete_view = login_required(DeleteQuestion.as_view())

submission_create_view = login_required(CreateSubmission.as_view())