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
        ('Private', 'Private - Only you can view'),
        ('Exclusive', 'Exclusive - Shared with your followers'),
        ('Public', 'Public - Anyone can view'),
    ]
    visibility = models.CharField(max_length=9, choices=visibility_choices, default='Private')
    created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    submitters = models.ManyToManyField(UserProfile, through='Submission')

    def __str__(self):
        return self.title

class Submission(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    submitter = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.submitter.user.first_name+' '+self.submitter.user.last_name+' - '+self.todo.title