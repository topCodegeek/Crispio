from django.db import models
from django.contrib.auth.models import User
from userProfile.models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    visibility_choices = [
        ('Private', 'Personal - Only visible to you'),
        ('Exclusive', 'Exclusive - Send to selective followers'),
        ('Public', 'Public - Send to your followers'),
    ]
    visibility = models.CharField(max_length=9, choices=visibility_choices, default='Private')
    created = models.DateTimeField(auto_now_add=True)
    important = models.BooleanField(default=False)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='author')
    submitters = models.ManyToManyField(UserProfile, through='Submission')
    send_to = models.ManyToManyField(UserProfile, related_name='send_to')

    def __str__(self):
        return self.title

class Submission(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    submitter = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.submitter.user.first_name+' '+self.submitter.user.last_name+' - '+self.todo.title