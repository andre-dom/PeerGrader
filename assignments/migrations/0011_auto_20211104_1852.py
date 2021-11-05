# Generated by Django 3.2.7 on 2021-11-05 01:52

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0010_alter_assignment_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradedassignmentsubmission',
            name='assignment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='graded_assignment_submissions', to='assignments.assignment'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 18, 52, 0, 785416, tzinfo=utc), validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2021, 11, 4, 18, 52, 0, 785416, tzinfo=utc))]),
        ),
    ]
