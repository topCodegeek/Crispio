from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(blank=True, null=True)
    pfp_url = models.URLField(blank=True, null=True)  # Store the profile picture URL
    instructing = models.ManyToManyField('self', related_name='instructingprofiles', symmetrical=False)
    following = models.ManyToManyField('self', related_name='followerprofiles', symmetrical=False)

    def __str__(self):
        return self.user.username