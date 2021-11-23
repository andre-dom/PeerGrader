# Generated by Django 3.2.7 on 2021-11-19 03:48

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0018_auto_20211112_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 19, 47, 59, 558810, tzinfo=utc), validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2021, 11, 18, 19, 47, 59, 558810, tzinfo=utc))]),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='state',
            field=django_fsm.FSMField(default='unpublished', max_length=50),
        ),
    ]
