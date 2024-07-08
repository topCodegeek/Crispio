from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.shortcuts import get_object_or_404
from userProfile.models import UserProfile
from django.utils import timezone
from .forms import TodoForm
from .models import Todo, Submission
# Create your views here.

def homepage(request):  #New User Required
    if request.user.is_authenticated:
        return redirect('currenttodos')
    return render (request, 'todoApp/homepage.html')

def connect(request):   #New User Required
    if request.user.is_authenticated:
        return redirect('currenttodos')
    return render (request, 'todoApp/connect.html')

def currentredirect(request):
    return redirect('currenttodos')

@login_required
def logoutuser(request): #login required
    if request.method == "POST":
        logout(request)
        return redirect ('homepage')
    else:
        return render (request, 'todoApp/currenttodos.html', {'error':'Strange logout request.'})     

@login_required
def createtodos(request):
    if request.method=='GET':
        return render (request, 'todoApp/createtodos.html', {'form':TodoForm})  
    else:
        profile=UserProfile.objects.get(user=request.user)
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.author = profile
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render (request, 'todoApp/createtodos.html', {'form':TodoForm, 'error':'Bad data passed in, please try again.'})  

@login_required
def currenttodos(request):
    profile = UserProfile.objects.get(user=request.user)
    todos = Todo.objects.filter(author=profile, submitters=None, visibility='Private').order_by('-created').exclude(visibility='Public')
    return render (request, 'todoApp/currenttodos.html', {'todos':todos,})

@login_required
def publictodos(request, Category):
    if Category=='following':
        profile = UserProfile.objects.get(user=request.user)
        following_profiles = profile.following.all()
        following_users = [profile for profile in following_profiles]
        todos = Todo.objects.filter(author__in=following_users, visibility='Exclusive').order_by('-created').exclude(id__in=Submission.objects.filter(submitter=profile).values('todo_id'))
        prev_author = 0
        withauthor = {}
        '''
        for todo in todos:
            if prev_author == todo.author.id:
                withauthor[todo.author.id]= '1'
            else:
                withauthor[todo.author.id]= '0'
            prev_author = todo.author.id
        '''
        context = {'todos': todos, 'withauthor':withauthor}
        return render(request, 'todoApp/exclusivetodos.html', context)

@login_required
def viewtodo(request, todo_id):
    profile = UserProfile.objects.get(user=request.user)
    todo1 = get_object_or_404(Todo, pk=todo_id)
    submissions = Submission.objects.filter(todo=todo1)
    submitted = Submission.objects.filter(todo=todo1, submitter=profile)
    count = Submission.objects.filter(todo=todo1).count()
    if profile in todo1.author.instructing.all():
        followed = True
    else:
        followed=False
    if todo1.visibility=='Exclusive' and followed==False and profile!=todo1.author:
        return redirect('currenttodos')
    if todo1.author==profile:
        self=True
    else:
        self=False
    form = TodoForm(instance=todo1)
    return render (request, 'todoApp/viewtodo.html', {'submitted':submitted, 'count':count, 'form':form, 'todo':todo1,'profile':profile,'self':self,'submissions':submissions})  

@login_required
def edittodo(request, todo_id):
    profile = UserProfile.objects.get(user=request.user)
    todo1 = get_object_or_404(Todo, pk=todo_id, author=profile)
    submitted = Submission.objects.filter(todo=todo1, submitter=profile)
    if request.method=="GET":
        form = TodoForm(instance=todo1)
        return render (request, 'todoApp/edittodo.html', {'todo':todo1,'form':form,'submitted':submitted})  
    else:
        try:
            form = TodoForm(request.POST, instance=todo1)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            form = TodoForm(instance=todo1)
            return render (request, 'todoApp/edittodo.html', {'submitted':submitted, 'form':form, 'todo':todo1, 'error':'Bad data passed in, please try again.'})  

@login_required
def completetodo(request, todo_id):
    profile = UserProfile.objects.get(user=request.user)
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method=='POST':
        submission = Submission.objects.create(todo=todo, submitter=profile, date_submitted=timezone.now())
        submission.save()
        return redirect('currenttodos')
    else:
        form = TodoForm(instance=todo)
        return render (request, 'todoApp/edittodo.html', {'todo':todo,'form':form, 'error':'Strange complete method.'})  

@login_required
def deletetodo(request, todo_id):
    profile = UserProfile.objects.get(user=request.user)
    todo = get_object_or_404(Todo, pk=todo_id, author=profile)
    if request.method=='POST':
        todo.delete()
        return redirect ('currenttodos')
    else:
        form = TodoForm(instance=todo)
        return render (request, 'todoApp/edittodo.html', {'todo':todo,'form':form, 'error':'Strange delete method.'})  

@login_required
def completedtodos(request):
    profile = UserProfile.objects.get(user=request.user)
    submissions = Submission.objects.filter(submitter=profile).order_by('-date_submitted')
    context={'submissions':submissions}
    return render (request, 'todoApp/completedtodos.html', context)