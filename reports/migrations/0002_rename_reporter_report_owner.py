# Generated by Django 4.2.13 on 2024-05-19 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='reporter',
            new_name='owner',
        ),
    ]
