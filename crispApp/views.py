from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from userProfile.models import UserProfile
from django.utils import timezone
from .forms import TodoForm
from .models import Todo, Submission
# Create your views here.

#New Visitors
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


#Logout
@login_required
def logoutuser(request): #login required
    if request.method == "POST":
        logout(request)
        return redirect ('homepage')
    else:
        return render (request, 'todoApp/currenttodos.html', {'error':'Strange logout request.'})     


#Create, Comeplete, Re-assign, Edit, Delete, 
@login_required #Profile needed
def createtodos(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect ('userProfile:createprofile')
    if request.method=='GET':
        return render (request, 'todoApp/createtodos.html', {'form':TodoForm})  
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.author = profile
            newtodo.save()
            if newtodo.visibility=='Exclusive':
                return redirect ('send_to', newtodo.id)
            else:
                return redirect('currenttodos')
        except ValueError:
            return render (request, 'todoApp/createtodos.html', {'form':TodoForm, 'error':'Bad data passed in, please try again.'})  
        
@login_required #Profile needed
def completetodo(request, todo_id):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect ('userProfile:createprofile')
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method=='POST':
        submission = Submission.objects.create(todo=todo, submitter=profile, date_submitted=timezone.now())
        submission.save()
        return redirect('currenttodos')
    else:
        form = TodoForm(instance=todo)
        return render (request, 'todoApp/edittodo.html', {'todo':todo,'form':form, 'error':'Strange complete method.'})  

@login_required
def reassign(request, todo_id):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect ('userProfile:createprofile')
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method=='GET':
        form = TodoForm(instance=todo)
        return render (request, 'todoApp/edittodo.html', {'todo':todo,'form':form})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.author = profile
            newtodo.save()
            if newtodo.visibility=='Exclusive':
                return redirect ('send_to', newtodo.id)
            else:
                return redirect('currenttodos')
        except ValueError:
            return render (request, 'todoApp/edittodo.html', {'form':form, 'todo':todo, 'error':'Bad data passed in, please try again.'}) 

@login_required #Profile needed
def edittodo(request, todo_id):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect ('userProfile:createprofile')
    todo1 = get_object_or_404(Todo, pk=todo_id, author=profile)
    if request.method=="GET":
        form = TodoForm(instance=todo1)
        return render (request, 'todoApp/edittodo.html', {'todo':todo1,'form':form})  
    else:
        try:
            form = TodoForm(request.POST, instance=todo1)
            form.save()
            if todo1.visibility=='Exclusive':
                return redirect ('send_to', todo1.id)
            else:
                return redirect('currenttodos')
        except ValueError:
            form = TodoForm(instance=todo1)
            return render (request, 'todoApp/edittodo.html', {'form':form, 'todo':todo1, 'error':'Bad data passed in, please try again.'})  

@login_required #Profile needed
def deletetodo(request, todo_id):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect ('userProfile:createprofile')
    todo = get_object_or_404(Todo, pk=todo_id, author=profile)
    if request.method=='POST':
        todo.delete()
        return redirect ('currenttodos')
    else:
        form = TodoForm(instance=todo)
        return render (request, 'todoApp/edittodo.html', {'todo':todo,'form':form, 'error':'Strange delete method.'})  
 
    
#Detail, Current, Following, Completed
@login_required #(DETAIL) - Profile Needed
def viewtodo(request, todo_id):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect ('userProfile:createprofile')
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
    if self or todo1.visibility=='Public' or profile in todo1.send_to.all():
        access = True
    else:
        access = False 
    context = {'submitted':submitted, 'count':count, 'form':form, 'todo':todo1,'profile':profile,'self':self,'submissions':submissions, 'access':access}
    return render (request, 'todoApp/viewtodo.html', context) 

@login_required #Profile needed
def currenttodos(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect ('userProfile:createprofile')
    todos = Todo.objects.filter(author=profile, submitters=None, visibility='Private').order_by('-created')
    return render (request, 'todoApp/currenttodos.html', {'todos':todos,})

@login_required #(FOLLOWING) - Profile needed
def publictodos(request, Category):
    if Category=='following':
        try:
            profile = UserProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect ('userProfile:createprofile')
        following_profiles = profile.following.all()
        following_users = [profile for profile in following_profiles]
        todos = Todo.objects.filter(author__in=following_users, visibility='Public').order_by('-created').exclude(id__in=Submission.objects.filter(submitter=profile).values('todo_id'))
        exclusive_todos = Todo.objects.filter(send_to=profile, visibility='Exclusive')
        todos |= exclusive_todos
        todos = todos.order_by('-created')
        withauthor = {}
        '''
        prev_author = 0
        for todo in todos:
            if prev_author == todo.author.id:
                withauthor[todo.author.id]= '1'
            else:
                withauthor[todo.author.id]= '0'
            prev_author = todo.author.id
        '''
        context = {'todos': todos, 'withauthor':withauthor}
        return render(request, 'todoApp/exclusivetodos.html', context)

@login_required #Profile needed
def completedtodos(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect ('userProfile:createprofile')
    submissions = Submission.objects.filter(submitter=profile).order_by('-date_submitted')
    context={'submissions':submissions}
    return render (request, 'todoApp/completedtodos.html', context)


#Send_to, Send(POST), Unsend(POST)
@login_required
def send_to(request, todo_id):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect ('userProfile:createprofile')
    todo = get_object_or_404(Todo, pk=todo_id, author=profile)
    if todo.author == profile:
        self=True
    if todo.visibility !='Exclusive':
        return redirect('viewtodo', todo_id)
    try:
        search_follower = request.GET['search_follower']
        instructing = profile.instructing.all().filter(name__contains=search_follower)
    except KeyError:
        instructing = profile.instructing.all()
    context={'todo':todo, 'instructing':instructing, 'self':self}
    if request.method=='GET':
        return render (request, 'todoApp/send_to.html', context)

@login_required
def send(request, todo_id, profile_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    todo = get_object_or_404(Todo, pk=todo_id, author=profile)
    send_to_profile = get_object_or_404(UserProfile, pk=profile_id)
    if request.method=='POST':
        todo.send_to.add(send_to_profile)
        return redirect ('send_to', todo.id)

@login_required
def unsend(request, todo_id, profile_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    todo = get_object_or_404(Todo, pk=todo_id, author=profile)
    send_to_profile = get_object_or_404(UserProfile, pk=profile_id)
    if request.method=='POST':
        todo.send_to.remove(send_to_profile)
        return redirect ('send_to', todo.id)

