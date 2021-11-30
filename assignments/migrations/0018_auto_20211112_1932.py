# Generated by Django 3.2.7 on 2021-11-13 03:32

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0017_auto_20211112_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentsubmission',
            name='score',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 13, 19, 32, 58, 374110, tzinfo=utc), validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2021, 11, 12, 19, 32, 58, 374110, tzinfo=utc))]),
        ),
    ]