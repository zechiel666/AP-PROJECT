# Generated by Django 5.1.5 on 2025-01-29 23:42

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_remove_course_examtime_course_examdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='examDate',
            field=django_jalali.db.models.jDateTimeField(null=True),
        ),
    ]
