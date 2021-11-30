# Generated by Django 3.2.7 on 2021-11-23 05:19

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0021_auto_20211122_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 23, 21, 19, 20, 700773, tzinfo=utc), validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2021, 11, 22, 21, 19, 20, 701768, tzinfo=utc))]),
        ),
    ]