from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'userProfile'

urlpatterns = [
     path('create/',views.createprofile, name='createprofile'),
     path('view/<int:profile_id>', views.viewprofile, name='viewprofile')
]