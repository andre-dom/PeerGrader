import pytz
from autoslug import AutoSlugField
from datetime import datetime, timedelta
from django_fsm import FSMField, transition

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import courses
import peerGrader

utc = pytz.UTC


class Assignment(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=utc.localize(datetime.now() + timedelta(days=1)),
                                    validators=[MinValueValidator(limit_value=utc.localize(datetime.now()))])
    course = models.ForeignKey('courses.Course', related_name='assignments', on_delete=models.CASCADE, )
    slug = AutoSlugField(populate_from='name', unique=True, editable=False)
    state = FSMField(default="unpublished", protected=True)

    @transition(field=state, source="unpublished", target="published")
    def to_state_published(self):
        # create assignment submissions for every student when assignment is published
        for student in self.course.students.all():
            assignment_submission = AssignmentSubmission.objects.create(student=student, assignment=self)
            for question in self.questions.all():
                QuestionSubmission.objects.create(AssignmentSubmission=assignment_submission, question=question)

    @transition(field=state, source="published", target="unpublished")
    def to_state_unpublished(self):
        # delete all associated assignment submissions when assignment is unpublished
        self.assignment_submissions.all().delete()

    def __str__(self):
        return self.name

    def numQuestions(self):
        return len(self.questions.all())

    def pointTotal(self):
        t = 0
        for q in self.questions.all():
            t += q.point_value
        return t


class Question(models.Model):
    question_body = models.TextField()
    point_value = models.IntegerField(validators=[MinValueValidator(0)])
    assignment = models.ForeignKey('Assignment', related_name='questions', on_delete=models.CASCADE, )
    index = models.IntegerField(validators=[MinValueValidator(1)])
    # ordering = ['index']

    # def getSubmissionByUser(self, user):
    #     assignment_submission = AssignmentSubmission.objects.get(student=user, assignment=self.assignment)
    #     question_submission = QuestionSubmission.objects.get(AssignmentSubmission=assignment_submission, question=self)
    #     return question_submission


class AssignmentSubmission(models.Model):
    student = models.ForeignKey(peerGrader.settings.AUTH_USER_MODEL,
                                related_name='submissions',
                                on_delete=models.CASCADE,
                                limit_choices_to={'is_instructor': False}, )
    assignment = models.ForeignKey('Assignment', related_name='assignment_submissions', on_delete=models.CASCADE, )
    score = models.IntegerField(default=-1, )
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.assignment.course.name + ", " + self.assignment.name + ": " + self.student.username


class QuestionSubmission(models.Model):
    answer_body = models.TextField()
    AssignmentSubmission = models.ForeignKey('AssignmentSubmission', related_name='question_submissions',
                                             on_delete=models.CASCADE, )
    question = models.ForeignKey('Question', related_name='question_submissions', on_delete=models.CASCADE, )
    points = models.IntegerField(default=-1, )
