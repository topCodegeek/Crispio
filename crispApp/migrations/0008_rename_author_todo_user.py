# Generated by Django 5.0.4 on 2024-06-20 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crispApp', '0007_rename_name_todo_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='author',
            new_name='user',
        ),
    ]