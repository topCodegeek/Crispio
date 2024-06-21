from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from .forms import TodoForm
from .models import Todo
# Create your views here.

def homepage(request):
    return render (request, 'todoApp/homepage.html')

def connect(request):
    return render (request, 'todoApp/connect.html')

def logoutuser(request): #login required
    if request.method == "POST":
        logout(request)
        return redirect ('homepage')
    else:
        return render (request, 'todoApp/currenttodos.html', {'error':'Bad logout method.'})     

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
    
def currenttodos(request):
    todos = Todo.objects.filter(author=request.user, date_completed__isnull=True)
    return render (request, 'todoApp/currenttodos.html', {'todos':todos})

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
    

