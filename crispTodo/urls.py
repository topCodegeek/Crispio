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

    #Allauth-Extra
    path('accounts/login/', views.currenttodos, name="currenttodos"),
    path('accounts/logout/', views.currenttodos, name="currenttodos"),
    path('accounts/password/change/', views.currenttodos, name="currenttodos"),
    path('accounts/password/set/', views.currenttodos, name="currenttodos"),
    path('accounts/password/reset/', views.currenttodos, name="currenttodos"),
    path('accounts/password/reset/done/', views.currenttodos, name="currenttodos"),
    path('accounts/password/reset/key/', views.currenttodos, name="currenttodos"),
    path('accounts/inactive/',views.currenttodos, name="currenttodos"),
    path('accounts/email/', views.currenttodos, name="currenttodos"),
    path('accounts/confirm-email/', views.currenttodos, name="currenttodos"),
    path('accounts/signup/', views.currenttodos, name="currenttodos"),
    path('accounts/signup/closed/', views.currenttodos, name="currenttodos"),

    #Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('accounts/', include('allauth.urls')),
    
    path('forget/', views.forgetpassword, name='forgetpassword'),

    #Todo
    path('', views.homepage, name="homepage"),
    path('current/', views.currenttodos, name="currenttodos"),
]
