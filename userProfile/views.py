from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from crispApp import views
from .models import UserProfile
from crispApp.models import Todo, Submission
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from allauth.socialaccount.models import SocialAccount

# Create your views here.

#Create
@login_required #Profile needed
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
          name1 = request.user.first_name+' '+request.user.last_name
          newprofile = UserProfile.objects.create(user=request.user, pfp_url=profile_picture_url, name=name1)
          newprofile.save()
     
     return redirect('currenttodos')

#Search Profile
@login_required
def searchprofile(request):
     userinput = request.GET['userinput']
     if userinput == '' or userinput == ' ' or userinput==None:
          profiles = None
     else:
          profiles = UserProfile.objects.filter(name__contains=userinput)
     context={'profiles':profiles}
     return render (request, 'userProfile/searchresult.html', context)

#View Profile
@login_required #Profile needed
def viewprofile(request, profile_id):
     try:
        request_profile = UserProfile.objects.get(user=request.user)
     except ObjectDoesNotExist:
        return redirect ('userProfile:createprofile')
     profile = get_object_or_404(UserProfile, pk=profile_id)
     todos = Todo.objects.exclude(id__in=Submission.objects.filter(submitter=request_profile).values('todo_id')).filter(visibility='Public', author=profile).order_by('-created')
     exclusive = Todo.objects.filter(author=profile, visibility='Exclusive', send_to=request_profile).order_by('-created').exclude(id__in=Submission.objects.filter(submitter=profile).values('todo_id'))
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

@login_required #Profile needed
def viewself(request):
     try:
        profile = UserProfile.objects.get(user=request.user)
     except ObjectDoesNotExist:
        return redirect ('userProfile:createprofile')
     todos = Todo.objects.filter(author=profile, visibility='Public').order_by('-created')
     exclusive = Todo.objects.filter(author=profile, visibility='Exclusive').order_by('-created')
     instructing = profile.instructing.all().count()
     following = profile.following.all().count()
     context = {'profile':profile, 'following':following,'instructing':instructing, 'todos':todos, 'exclusive':exclusive}
     return render (request, 'userProfile/viewself.html', context)


#Follow and Unfollow
@login_required #Profile needed
def  follow(request, profile_id):
     if request.method=='POST':
          to_follow = get_object_or_404(UserProfile, pk=profile_id)
          try:
               request_profile = UserProfile.objects.get(user=request.user)
          except ObjectDoesNotExist:
               return redirect ('userProfile:createprofile')
          to_follow.instructing.add(request_profile)
          request_profile.following.add(to_follow)
          return redirect('userProfile:viewprofile', profile_id)

@login_required #Profile needed
def  unfollow(request, profile_id):
     if request.method=='POST':
          to_follow = get_object_or_404(UserProfile, pk=profile_id)
          try:
               request_profile = UserProfile.objects.get(user=request.user)
          except ObjectDoesNotExist:
               return redirect ('userProfile:createprofile')
          to_follow.instructing.remove(request_profile)
          request_profile.following.remove(to_follow)
          return redirect('userProfile:viewprofile', profile_id)
     

#Following and Instructing
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