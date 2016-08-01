from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from ..reddit.models import Thread, Comment
from .forms import ProfileChangeForm

def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        next_url = request.POST.get('next', '/')
        if form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(next_url)
    else:
        next_url = request.GET.get('next')

    return render(request, 'login.html', {'form': form, 'next': next_url})

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            uname = form.cleaned_data['username']
            passwd = form.cleaned_data['password1']
            new_user = auth.authenticate(username=uname, password=passwd)
            auth.login(request, new_user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_threads = Thread.objects.filter(author=user).order_by('-created_on')[:5]
    comment_num = Comment.objects.filter(author=user).count()
    user_comments = Comment.objects.filter(author=user).order_by('-created_on')[:5]
    return render(request, 'profile.html', {'profile_user': user,
                                            'threads': user_threads,
                                            'comment_num': comment_num,
                                            'comments': user_comments})

@login_required
def change_profile(request, username):
    if username != request.user.get_username():
        return HttpResponseForbidden

    old_email = get_object_or_404(User, username=username).email
    profile_change_form = ProfileChangeForm(prefix='profile',
                                            initial={'email': old_email})
    passwd_change_form = PasswordChangeForm(username, prefix='passwd')

    if request.method == 'POST':
        if any(['profile' in key for key in request.POST.keys()]):
            profile_change_form = ProfileChangeForm(request.POST, prefix='profile')
            if profile_change_form.is_valid():
                user = request.user
                user.email = profile_change_form.cleaned_data['email']
                user.save()

        if any(['passwd' in key for key in request.POST.keys()]):
            passwd_change_form = PasswordChangeForm(data=request.POST,
                                                    user=request.user, prefix='passwd')
            if passwd_change_form.is_valid():
                passwd_change_form.save()
                auth.update_session_auth_hash(request, passwd_change_form.user)

    return render(request, 'profile_change.html', {'form_profile': profile_change_form,
                                                   'form_passwd': passwd_change_form})
