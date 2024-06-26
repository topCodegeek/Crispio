from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pfp_url = models.URLField(blank=True, null=True)  # Store the profile picture URL
    instructing = models.ManyToManyField(User, related_name='instructing')
    following = models.ManyToManyField(User, related_name='followers')

    def __str__(self):
        return self.user.username