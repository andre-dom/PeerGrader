import pytz
from autoslug import AutoSlugField
from datetime import datetime, timedelta

from django.core.validators import MinValueValidator
from django.db import models
import courses

utc = pytz.UTC


class Assignment(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=utc.localize(datetime.now() + timedelta(days=1)),
                                    validators=[MinValueValidator(limit_value=utc.localize(datetime.now()))])
    course = models.ForeignKey('courses.Course', related_name='assignments', on_delete=models.CASCADE, )
    slug = AutoSlugField(populate_from='name', unique=True, editable=False)

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
