# Generated by Django 5.0.4 on 2024-08-12 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0006_userprofile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]
