# Generated by Django 3.2.7 on 2021-10-31 02:39

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignments', '0008_auto_20211028_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 19, 39, 36, 308692, tzinfo=utc), validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2021, 10, 30, 19, 39, 36, 308692, tzinfo=utc))]),
        ),
        migrations.CreateModel(
            name='GradedQuestionSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=-1)),
                ('GradedAssignmentSubmission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='graded_question_submissions', to='assignments.assignmentsubmission')),
                ('QuestionSubmission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='graded_question_submissions', to='assignments.questionsubmission')),
            ],
        ),
        migrations.CreateModel(
            name='GradedAssignmentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_submitted', models.BooleanField(default=False)),
                ('assignment_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='graded_assignment_submissions', to='assignments.assignmentsubmission')),
                ('grader', models.ForeignKey(limit_choices_to={'is_instructor': False}, on_delete=django.db.models.deletion.CASCADE, related_name='peer_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]