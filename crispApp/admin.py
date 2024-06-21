from django.contrib import admin
from .models import UserProfile, Todo
# Register your models here.

class TodoAdmin(admin.ModelAdmin):
     readonly_fields = ('created','author')
admin.site.register(UserProfile)
admin.site.register(Todo, TodoAdmin)