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

    #Auth
    path('connect/', views.connect, name='connect'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('accounts/', include('allauth.urls')),
    
    #Todo - View
    path('', views.homepage, name="homepage"),
    path('todos/current/', views.currenttodos, name="currenttodos"),
    path('todos/completed/', views.completedtodos, name="completedtodos"),
    #todo - Action
    path('todo/create/', views.createtodos, name="createtodos"),
    path('todo/edit/<int:todo_id>', views.edittodo, name="edittodo"),
    path('todo/complete/<int:todo_id>', views.completetodo, name="completetodo"),
    path('todo/delete/<int:todo_id>', views.deletetodo, name="deletetodo"),
]
