# Generated by Django 3.2.7 on 2021-10-01 03:35

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 1, 20, 35, 49, 730886, tzinfo=utc), validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2021, 9, 30, 20, 35, 49, 730886, tzinfo=utc))]),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_body', models.TextField()),
                ('point_value', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('index', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='assignments.assignment')),
            ],
        ),
    ]
