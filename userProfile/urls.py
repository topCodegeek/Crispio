from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'userProfile'

urlpatterns = [
     path('create/',views.createprofile, name='createprofile'),
     path('view/<int:profile_id>', views.viewprofile, name='viewprofile'),
     path('view/self/', views.viewself, name='viewself'),
     path('follow/<int:profile_id>', views.follow, name='follow'),
     path('unfollow/<int:profile_id>', views.unfollow, name='unfollow'),
     path('view/<int:profile_id>/instructing/', views.instructing, name='instructing'),      
     path('view/<int:profile_id>/following/', views.following, name='following'),                   
]