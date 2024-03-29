from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import todowooAppForm
from .models import todowooApp
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'todowooApp/home.html')

    
    return render(request, 'viewtodo.html', context)

def signupuser(request):                                      
    if request.method == 'GET':
        return render(request, 'todowooApp/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todowooApp/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todowooApp/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todowooApp/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todowooApp/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')



@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todowooApp/createtodo.html', {'form':todowooAppForm()})
    else:
        try:
            form = todowooAppForm(request.POST)
            newtodowooApp = form.save(commit=False)
            newtodowooApp.user = request.user
            newtodowooApp.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todowooApp/createtodo.html', {'form':todowooAppForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def currenttodos(request):
    todowooApps = todowooApp.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todowooApp/currenttodos.html', {'todowooApps':todowooApps})

@login_required
def completedtodos(request):
    todowooApps = todowooApp.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todowooApp/completedtodos.html', {'todowooApps':todowooApps})

@login_required
def viewtodo(request, todowooApp_pk):
    todowooApp = get_object_or_404(todowooApp, pk=todowooApp_pk, user=request.user)
    if request.method == 'GET':
        form = todowooAppForm(instance=todowooApp)
        return render(request, 'todowooApp/viewtodo.html', {'todowooApp':todowooApp, 'form':form})
    else:
        try:
            form = todowooAppForm(request.POST, instance=todowooApp)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todowooApp/viewtodo.html', {'todowooApp':todowooApp, 'form':form, 'error':'Bad info'})

@login_required
def completetodowooApp(request, todowooApp_pk):
    todowooApp = get_object_or_404(todowooApp, pk=todowooApp_pk, user=request.user)
    if request.method == 'POST':
        todowooApp.datecompleted = timezone.now()
        todowooApp.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todowooApp_pk):
    todowooApp = get_object_or_404(todowooApp, pk=todowooApp_pk, user=request.user)
    if request.method == 'POST':
        todowooApp.delete()
        return redirect('currenttodos')
