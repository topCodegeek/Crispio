from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignupForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404
from .models import UserProfile
# Create your views here.

def signupuser(request):
    if request.method == "GET":
        return render (request, 'todoApp/signupuser.html', {'form': SignupForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['first_name']+request.POST['last_name'], password=request.POST['password1'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render (request, 'todoApp/signupuser.html', {'form': SignupForm, 'error':'Credentials already exists.'})
        else:
            return render (request, 'todoApp/signupuser.html', {'form': SignupForm, 'error':'Passwords didn\'t match.'})


def logoutuser(request): #login required
    if request.method == "POST":
        logout(request)
        return redirect ('homepage')
    else:
        return render (request, 'todoApp/currenttodos.html', {'error':'Bad logout method.'})

def loginuser(request):
    if request.method == "GET":
        return render (request, 'todoApp/loginuser.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
           return render (request, 'todoApp/loginuser.html', {'form': AuthenticationForm, 'error':'Credentials didn\'t match or user doesn\'t exist.'})
        else:
            login(request, user)
            return redirect('currenttodos')      

def forgetpassword(request):
    return render (request, 'todoApp/forgetpassword.html')

def currenttodos(request):
    return render (request, 'todoApp/currenttodos.html')

def homepage(request):
    return render (request, 'todoApp/homepage.html')