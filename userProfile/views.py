from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from crispApp import views
from .models import UserProfile
from crispApp.models import Todo, Submission
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

@login_required
def viewprofile(request, profile_id):
     profile = get_object_or_404(UserProfile, pk=profile_id)
     request_profile = UserProfile.objects.get(user=request.user)  # Assuming you have a one-to-one relation with UserProfile
     todos = Todo.objects.exclude(id__in=Submission.objects.filter(submitter=request_profile).values('todo_id')).filter(visibility='Public', author=profile)
     exclusive = Todo.objects.filter(author=profile, visibility='Exclusive').order_by('-created').exclude(id__in=Submission.objects.filter(submitter=profile).values('todo_id'))
     instructing = profile.instructing.all().count()
     following = profile.following.all().count()
     if request_profile in profile.instructing.all():
          followed = True
          self=False
     elif request.user==profile.user:
          followed = False
          self=True
     else:
          followed = False
          self = False
     context = {'exclusive':exclusive, 'todos': todos, 'profile':profile,'followed':followed,'self':self, 'instructing':instructing,'following':following}
     return render (request, 'userProfile/viewprofile.html', context)

@login_required
def instructing(request, profile_id):
     profile = get_object_or_404(UserProfile, pk=profile_id)
     instructing = profile.instructing.all()
     instructing_count = instructing.count()
     return render (request, 'userProfile/instructing.html', {'profile':profile, 'instructing':instructing, 'count':instructing_count})

@login_required
def following(request, profile_id):
     profile = get_object_or_404(UserProfile, pk=profile_id)
     following = profile.following.all()
     following_count = following.count()
     return render (request, 'userProfile/following.html', {'profile':profile, 'following':following, 'count':following_count})

@login_required
def viewself(request):
     profile = get_object_or_404(UserProfile, user=request.user)
     todos = Todo.objects.filter(author=profile, visibility='Public')
     exclusive = Todo.objects.filter(author=profile, visibility='Exclusive')
     instructing = profile.instructing.all().count()
     following = profile.following.all().count()
     context = {'profile':profile, 'following':following,'instructing':instructing, 'todos':todos, 'exclusive':exclusive}
     return render (request, 'userProfile/viewself.html', context)

@login_required
def  follow(request, profile_id):
     if request.method=='POST':
          to_follow = get_object_or_404(UserProfile, pk=profile_id)
          request_profile = get_object_or_404(UserProfile, user=request.user)
          to_follow.instructing.add(request_profile)
          request_profile.following.add(to_follow)
          return redirect('userProfile:viewprofile', profile_id)

@login_required
def  unfollow(request, profile_id):
     if request.method=='POST':
          to_follow = get_object_or_404(UserProfile, pk=profile_id)
          request_profile = get_object_or_404(UserProfile, user=request.user)
          to_follow.instructing.remove(request_profile)
          request_profile.following.remove(to_follow)
          return redirect('userProfile:viewprofile', profile_id)