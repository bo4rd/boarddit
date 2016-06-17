from django.shortcuts import render, get_object_or_404
from .models import Thread, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError, HttpResponse
from .forms import ThreadSubmitForm

def index(request):
    return render(request, 'index.html', {'threads': Thread.objects.all()})

def show_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponse(status=403)
        try:
            new_comment = Comment(author=request.user, thread=thread,
                                  text=request.POST['text'])
            parent_comment_id = int(request.POST['ancestor'])
            if parent_comment_id > 0:
                parent_comment = Comment.objects.get(id=parent_comment_id)
            else:
                parent_comment = None
            new_comment.insert_at(parent_comment, position='last-child', save=True)
        except:
            return HttpResponse(status=500)
        return HttpResponse(status=200)
    else:
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
