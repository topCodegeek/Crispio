from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import TodoForm
from .models import Todo
# Create your views here.

def homepage(request):
    return render (request, 'todoApp/homepage.html')

def connect(request):
    return render (request, 'todoApp/connect.html')

def currentredirect(request):
    return redirect('currenttodos')

@login_required
def logoutuser(request): #login required
    if request.method == "POST":
        logout(request)
        return redirect ('homepage')
    else:
        return render (request, 'todoApp/currenttodos.html', {'error':'Bad logout method.'})     

@login_required
def createtodos(request):
    if request.method=='GET':
        return render (request, 'todoApp/createtodos.html', {'form':TodoForm})  
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.author = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render (request, 'todoApp/createtodos.html', {'form':TodoForm, 'error':'Bad data passed in, please try again.'})  

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(author=request.user, date_completed__isnull=True).order_by('-created')
    return render (request, 'todoApp/currenttodos.html', {'todos':todos})

@login_required
def edittodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, author=request.user)
    if request.method=="GET":
        form = TodoForm(instance=todo)
        return render (request, 'todoApp/edittodo.html', {'todo':todo,'form':form})  
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            form = TodoForm(instance=todo)
            return render (request, 'todoApp/edittodo.html', {'form':form, 'todo':todo, 'error':'Bad data passed in, please try again.'})  

@login_required
def completetodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, author=request.user)
    if request.method=='POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currenttodos')
    else:
        form = TodoForm(instance=todo)
        return render (request, 'todoApp/edittodo.html', {'todo':todo,'form':form, 'error':'Strange complete method.'})  

@login_required
def deletetodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, author=request.user)
    if request.method=='POST':
        todo.delete()
        return redirect ('currenttodos')
    else:
        form = TodoForm(instance=todo)
        return render (request, 'todoApp/edittodo.html', {'todo':todo,'form':form, 'error':'Strange delete method.'})  

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(author=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render (request, 'todoApp/completedtodos.html', {'todos':todos})