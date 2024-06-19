from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404
# Create your views here.

def connect(request):
    return render (request, 'todoApp/connect.html')

def logoutuser(request): #login required
    if request.method == "POST":
        logout(request)
        return redirect ('homepage')
    else:
        return render (request, 'todoApp/currenttodos.html', {'error':'Bad logout method.'})     

def currenttodos(request):
    return render (request, 'todoApp/currenttodos.html')

def homepage(request):
    return render (request, 'todoApp/homepage.html')
