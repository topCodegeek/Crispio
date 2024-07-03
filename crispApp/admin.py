from django.contrib import admin
from .models import Todo, Submission
# Register your models here.

class TodoAdmin(admin.ModelAdmin):
     readonly_fields = ('created','author')
admin.site.register(Todo, TodoAdmin)
admin.site.register(Submission)