# Generated by Django 5.1.5 on 2025-01-30 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_examtime_alter_course_examdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
