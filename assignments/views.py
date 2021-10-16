from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from assignments.models import Assignment, Question, AssignmentSubmission, QuestionSubmission
from courses.models import Course


class AssignmentView(DetailView):
    model = Assignment
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

    def get_template_names(self):
        if self.request.user.is_instructor:
            return 'assignments/instructor_assignment_view.html'
        else:
            return 'assignments/student_assignment_view.html'

    # if student, pass assignment submission to context so they can preview their answers
    def get_context_data(self, **kwargs):
        context = super(AssignmentView, self).get_context_data(**kwargs)
        user = self.request.user
        if not user.is_instructor:
            assignment = Assignment.objects.get(slug=self.kwargs['slug'])
            assignment_submission = AssignmentSubmission.objects.get(student=user, assignment=assignment)
            context.update({"assignment_submission": assignment_submission})
        return context

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
    slug_url_kwarg = 'slug'  # use slug to get specific assignment
    slug_field = 'slug'
    success_url = "/"  # sending to home page
    template_name = 'assignments/editassignment.html'
    fields = ('name', 'due_date',)  # specifying what variables in the model need to be modified


class PublishAssignment(UpdateView):
    model = Assignment
    template_name = 'assignments/publish_assignment.html'
    fields = ('is_published',)
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = "/"

    def form_valid(self, form):
        # create/delete assignment submissions for every student when assignments are published/unpublished
        assignment = Assignment.objects.get(slug=self.kwargs['slug'])
        if form.instance.is_published:
            for student in assignment.course.students.all():
                assignment_submission = AssignmentSubmission.objects.create(student=student, assignment=assignment)
                for question in assignment.questions.all():
                    QuestionSubmission.objects.create(AssignmentSubmission=assignment_submission, question=question)
        else:
            assignment.assignment_submissions.all().delete()
        return super(PublishAssignment, self).form_valid(form)

    # def clean(self):
    #     assignment = Assignment.objects.get(slug=self.kwargs['slug'])
    #     if assignment.questions.get_values().len() == 0:
    #         raise forms.ValidationError("No questions in assignment")

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


class EditQuestionSubmission(UpdateView):
    model = QuestionSubmission
    template_name = 'submissions/edit_question_submission.html'
    fields = ('answer_body',)
    success_url = "/"

    def get_object(self):
        assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        assignment_submission = AssignmentSubmission.objects.get(assignment=assignment, student=self.request.user)
        question = Question.objects.get(assignment=assignment, index=self.kwargs['index'])
        question_submission = QuestionSubmission.objects.get(AssignmentSubmission=assignment_submission,
                                                             question=question)
        return question_submission

    def dispatch(self, request, *args, **kwargs):
        # validate user
        assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        course = assignment.course
        user = request.user
        if user not in course.students.all():
            return redirect('/')
        else:
            return super(EditQuestionSubmission, self).dispatch(request, *args, **kwargs)


class SubmitSubmission(UpdateView):
    model = AssignmentSubmission
    template_name = 'submissions/submit_submission.html'
    fields = ('is_submitted',)
    success_url = "/"

    def get_object(self):
        assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        assignment_submission = AssignmentSubmission.objects.get(assignment=assignment, student=self.request.user)
        return assignment_submission

    def dispatch(self, request, *args, **kwargs):
        # validate user
        assignment = Assignment.objects.get(slug=self.kwargs['assignment_slug'])
        course = assignment.course
        user = request.user
        if user not in course.students.all():
            return redirect('/')
        else:
            return super(SubmitSubmission, self).dispatch(request, *args, **kwargs)


assignment_detail_view = login_required(AssignmentView.as_view())
assignment_create_view = login_required(CreateAssignment.as_view())
assignment_delete_view = login_required(DeleteAssignment.as_view())
assignment_publish_view = login_required(PublishAssignment.as_view())
assignment_edit_view = login_required(EditAssignment.as_view())

question_edit_view = login_required(EditQuestion.as_view())
question_create_view = login_required(CreateQuestion.as_view())
question_delete_view = login_required(DeleteQuestion.as_view())

question_submission_edit_view = login_required(EditQuestionSubmission.as_view())
submit_submission_view = login_required(SubmitSubmission.as_view())