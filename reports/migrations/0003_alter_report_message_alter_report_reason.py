# Generated by Django 4.2.13 on 2024-05-23 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_rename_reporter_report_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='message',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='report',
            name='reason',
            field=models.CharField(max_length=150),
        ),
    ]