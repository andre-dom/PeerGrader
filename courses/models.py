from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField

import peerGrader.settings


class Course(models.Model):
    name = models.CharField(max_length=30)
    instructor = models.ForeignKey(peerGrader.settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   limit_choices_to={'is_instructor': True},
                                   related_name='taught_class')
    students = models.ManyToManyField(peerGrader.settings.AUTH_USER_MODEL,
                                      limit_choices_to={'is_instructor': False},
                                      related_name='enrolled_class')
    slug = AutoSlugField(populate_from='name', unique=True, editable=False)

    def __str__(self):
        return self.name
