"""
URL configuration for crispTodo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from crispApp import views
from allauth.account.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userprofile/', include('userProfile.urls')),

    #Allauth - Unnecessary
    path('accounts/signup/', views.currentredirect, name="currentredirect"),
    path('accounts/login/', views.currentredirect, name="currentredirect"),
    path('accounts/logout/', views.currentredirect, name="currentredirect"),
    path('accounts/confirm-email/', views.currentredirect, name="currentredirect"),
    path('accounts/password/reset/', views.currentredirect, name="currentredirect"),
    path('accounts/password/reset/done/', views.currentredirect, name="currentredirect"),
    path('accounts/password/reset/complete/', views.currentredirect, name="currentredirect"),
    path('accounts/password/change/', views.currentredirect, name="currentredirect"),
    path('accounts/password/change/done/', views.currentredirect, name="currentredirect"),
    path('accounts/inactive/', views.currentredirect, name="currentredirect"),
    path('accounts/profile/', views.currentredirect, name="currentredirect"),

    #Auth
    path('connect/', views.connect, name='connect'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('accounts/', include('allauth.urls')),
    
    #Todo - View
    path('', views.homepage, name="homepage"),
    path('todos/current/', views.currenttodos, name="currenttodos"),
    path('todos/current/<str:Category>', views.publictodos, name="publictodos"),
    path('todos/completed/', views.completedtodos, name="completedtodos"),
    path('todo/create/', views.createtodos, name="createtodos"),
    path('todo/view/<int:todo_id>', views.viewtodo, name="viewtodo"),
    path('todo/edit/<int:todo_id>', views.edittodo, name="edittodo"),
    path('todo/reassign/<int:todo_id>', views.reassign, name="reassign"),
    path('todo/send_to/<int:todo_id>', views.send_to, name="send_to"),
    path('todo/send/<int:todo_id>/<int:profile_id>', views.send, name="send"),
    path('todo/unsend/<int:todo_id>/<int:profile_id>', views.unsend, name="unsend"),
    path('todo/complete/<int:todo_id>', views.completetodo, name="completetodo"),
    path('todo/delete/<int:todo_id>', views.deletetodo, name="deletetodo"),
]
