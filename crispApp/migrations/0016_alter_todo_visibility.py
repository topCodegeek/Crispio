# Generated by Django 5.0.4 on 2024-07-07 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crispApp', '0015_alter_todo_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='visibility',
            field=models.CharField(choices=[('Private', 'Private - Only you can view'), ('Exclusive', 'Exclusive - Sent to your followers'), ('Public', 'Public - Displayed on your profile')], default='Private', max_length=9),
        ),
    ]
