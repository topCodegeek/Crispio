# Generated by Django 5.0.4 on 2024-08-12 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crispApp', '0020_alter_todo_complete_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='Pin',
            field=models.BooleanField(default=False),
        ),
    ]