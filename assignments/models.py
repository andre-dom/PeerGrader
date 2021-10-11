import pytz
from autoslug import AutoSlugField
from datetime import datetime, timedelta

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
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def numQuestions(self):
        return len(self.questions.values())

    def pointTotal(self):
        t = 0
        for q in self.questions:
            t += q.point_value
        return t


class Question(models.Model):
    question_body = models.TextField()
    point_value = models.IntegerField(validators=[MinValueValidator(0)])
    assignment = models.ForeignKey('Assignment', related_name='questions', on_delete=models.CASCADE, )
    index = models.IntegerField(validators=[MinValueValidator(1)])


class AssignmentSubmission(models.Model):
    student = models.ForeignKey(peerGrader.settings.AUTH_USER_MODEL, related_name='submissions', on_delete=models.CASCADE, )
    assignment = models.ForeignKey('Assignment', related_name='assignment_submissions', on_delete=models.CASCADE, )
    score = models.IntegerField(validators=[MinValueValidator(0), ], )


class QuestionSubmission(models.Model):
    answer_body = models.TextField()
    AssignmentSubmission = models.ForeignKey('AssignmentSubmission', related_name='question_submissions', on_delete=models.CASCADE, )
    question = models.ForeignKey('Question', related_name='question_submissions', on_delete=models.CASCADE, )
    points = models.IntegerField(validators=[MinValueValidator(0), ],)
