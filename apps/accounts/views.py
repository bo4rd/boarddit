from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from ..reddit.models import Thread, Comment

def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/')

    return render(request, 'login.html', {'form': form})

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_threads = Thread.objects.filter(author=user).order_by('-created_on')[:5]
    comment_num = Comment.objects.filter(author=user).count()
    return render(request, 'profile.html', {'profile_user': user, 'threads':
                                            user_threads, 'comment_num':
                                            comment_num})
