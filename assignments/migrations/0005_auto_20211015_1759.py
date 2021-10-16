# Generated by Django 3.2.7 on 2021-10-16 00:59

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignments', '0004_auto_20211010_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='is_submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 16, 17, 59, 18, 238742, tzinfo=utc), validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2021, 10, 15, 17, 59, 18, 238742, tzinfo=utc))]),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='student',
            field=models.ForeignKey(limit_choices_to={'is_instructor': False}, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL),
        ),
    ]
