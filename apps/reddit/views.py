from django.shortcuts import render, get_object_or_404
from .models import Thread, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import ThreadSubmitForm

def index(request):
    return render(request, 'index.html', {'threads': Thread.objects.all()})

def show_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    return render(request, 'thread.html', {'thread': thread,
                                           'nodes': Comment.objects.all()})

@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ThreadSubmitForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['link']
            new_thread = Thread(author=request.user, title=form.cleaned_data['title'],
                                text=form.cleaned_data['text'], url=url)
            new_thread.save()
            return HttpResponseRedirect(new_thread.permalink)
    else:
        form = ThreadSubmitForm()

    return render(request, 'create_thread.html', {'form': form})

def user_profile(request, username):
    user = User.objects.get(username=username)
    user_threads = Thread.objects.filter(author=user).order_by('-created_on')[:5]
    comment_num = Comment.objects.filter(author=user).count()
    return render(request, 'profile.html', {'profile_user': user, 'threads':
                                            user_threads, 'comment_num':
                                            comment_num})
