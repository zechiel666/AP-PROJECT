# Generated by Django 5.1.5 on 2025-02-04 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_course_hamniaz_course_pishniaz'),
        ('user', '0002_user_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(blank=True, to='courses.course'),
        ),
    ]
