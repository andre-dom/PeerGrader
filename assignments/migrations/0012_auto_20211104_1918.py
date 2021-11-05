# Generated by Django 3.2.7 on 2021-11-05 02:18

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0011_auto_20211104_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='submitted_at',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 19, 18, 50, 326589, tzinfo=utc), validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2021, 11, 4, 19, 18, 50, 326589, tzinfo=utc))]),
        ),
    ]