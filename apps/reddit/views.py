from django.shortcuts import render, get_object_or_404
from .models import Thread, Comment, Subreddit
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError, HttpResponse
from .forms import ThreadSubmitForm

def index(request):
    return render(request, 'thread_list.html', {'threads': Thread.objects.all(),
                                                'subreddits': Subreddit.objects.all()})


def show_thread(request, subreddit_id, subreddit_slug, thread_id, thread_slug):
    thread = get_object_or_404(Thread, id=thread_id)
    subreddit = get_object_or_404(Subreddit, id=subreddit_id)

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
        return render(request, 'thread.html', {'subreddits': Subreddit.objects.all(),
                                               'current_subreddit': subreddit,
                                               'thread': thread,
                                               'nodes': Comment.objects.all()})


@login_required
def create_thread(request,subreddit_id, subreddit_slug):
    subreddit = get_object_or_404(Subreddit, id=subreddit_id)

    if request.method == 'POST':
        form = ThreadSubmitForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['link']
            new_thread = Thread(author=request.user, title=form.cleaned_data['title'],
                                text=form.cleaned_data['text'], url=url,
                                subreddit=subreddit)
            new_thread.save()
            return HttpResponseRedirect(new_thread.permalink)
    else:
        form = ThreadSubmitForm()

    return render(request, 'create_thread.html', {'subreddits': Subreddit.objects.all(),
                                                  'current_subreddit': subreddit,
                                                  'form': form})


def show_subreddit(request, subreddit_id, subreddit_slug):
    subreddit = get_object_or_404(Subreddit, id=subreddit_id)
    threads = Thread.objects.filter(subreddit=subreddit)
    return render(request, 'thread_list.html', {'subreddits': Subreddit.objects.all(),
                                                'current_subreddit': subreddit,
                                                'threads': threads})
