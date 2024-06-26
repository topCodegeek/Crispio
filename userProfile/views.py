from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from crispApp import views
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from allauth.socialaccount.models import SocialAccount

# Create your views here.
@login_required
def createprofile(request):
     try:
          userprofile = UserProfile.objects.get(user=request.user)
     except ObjectDoesNotExist:
          social_account = SocialAccount.objects.get(user=request.user)
          extra_data = social_account.extra_data
          if social_account.provider == 'google':
               profile_picture_url = extra_data.get('picture') # Google
          elif social_account.provider == 'github':
               profile_picture_url = extra_data.get('avatar_url')  # GitHub
          elif social_account.provider == 'twitter':
               profile_picture_url = extra_data.get('profile_image_url') # Twitter
          else:
               profile_picture_url = None
          newprofile = UserProfile.objects.create(user=request.user, pfp_url=profile_picture_url)
          newprofile.save()
     
     return redirect('currenttodos')

def viewprofile(request, profile_id):
     profile = get_object_or_404(UserProfile, pk=profile_id)
     return render (request, 'userProfile/viewprofile.html', {'profile':profile})
