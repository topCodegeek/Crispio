from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, db_index=True)
    profile_picture = models.ImageField(upload_to = "media/crispApp/images/", null=True)
    pfp_url = models.URLField(blank=True, null=True)  # Store the profile picture URL
    instructing = models.ManyToManyField(User, related_name='instructing')
    following = models.ManyToManyField(User, related_name='followers')

    def __str__(self):
        return self.user.username
