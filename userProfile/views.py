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
     if request.user in profile.instructing.all():
          followed = True
          self=False
     elif request.user==profile.user:
          followed = False
          self=True
     else:
          followed = False
          self = False
     return render (request, 'userProfile/viewprofile.html', {'profile':profile,'followed':followed,'self':self})

@login_required
def viewself(request):
     profile = get_object_or_404(UserProfile, user=request.user)
     return render (request, 'userProfile/viewself.html', {'profile':profile})

@login_required
def  follow(request, profile_id):
     if request.method=='POST':
          to_follow = get_object_or_404(UserProfile, pk=profile_id)
          to_follow.instructing.add(request.user)
          request_profile = get_object_or_404(UserProfile, user=request.user)
          request_profile.following.add(to_follow.user)

          if request.user in to_follow.instructing.all():
               followed = True
               self=False
          elif request.user==to_follow.user:
               followed = False
               self=True
          else:
               followed = False
               self = False
          return render (request, 'userProfile/viewprofile.html', {'profile':to_follow, 'followed':followed,'self':self})

@login_required
def  unfollow(request, profile_id):
     if request.method=='POST':
          to_follow = get_object_or_404(UserProfile, pk=profile_id)
          to_follow.instructing.remove(request.user)
          request_profile = get_object_or_404(UserProfile, user=request.user)
          request_profile.following.remove(to_follow.user)

          if request.user in to_follow.instructing.all():
               followed = True
               self=False
          elif request.user==to_follow.user:
               followed = False
               self=True
          else:
               followed = False
               self = False
          return render (request, 'userProfile/viewprofile.html', {'profile':to_follow, 'followed':followed,'self':self})          