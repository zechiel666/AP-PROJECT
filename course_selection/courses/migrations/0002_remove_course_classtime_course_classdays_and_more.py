# Generated by Django 5.1.5 on 2025-01-29 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='classTime',
        ),
        migrations.AddField(
            model_name='course',
            name='classDays',
            field=models.CharField(choices=[('شنبه/دوشنبه', 'شنبه/دوشنبه'), ('یکشنبه/سشنبه', 'یکشنبه/سشنبه')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='endTime',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='startTime',
            field=models.TimeField(null=True),
        ),
    ]
