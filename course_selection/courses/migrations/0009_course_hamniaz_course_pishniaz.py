# Generated by Django 5.1.5 on 2025-02-04 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_course_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='hamniaz',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='pishniaz',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
