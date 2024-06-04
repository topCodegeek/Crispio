from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
# Create your views here.

def signupuser(request):
    if request.method == "GET":
        return render (request, 'todoApp/signupuser.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render (request, 'todoApp/signupuser.html', {'form': UserCreationForm, 'error':'Username already exists.'})
        else:
            return render (request, 'todoApp/signupuser.html', {'form': UserCreationForm, 'error':'Passwords didn\'t match.'})

#login required
def logoutuser(request):
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

def currenttodos(request):
    return render (request, 'todoApp/currenttodos.html')

def homepage(request):
    return render (request, 'todoApp/homepage.html')