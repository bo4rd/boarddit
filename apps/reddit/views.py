from django.shortcuts import render, get_object_or_404
from .models import Thread, Comment, Subreddit
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseServerError, HttpResponse, JsonResponse
from .forms import ThreadSubmitForm

MAX_COMMENT_LEVEL = 7

def index(request):
    return render(request, 'thread_list.html', {'threads': Thread.objects.all(),
                                                'subreddits': Subreddit.objects.all()})


def show_subreddit(request, subreddit_id, subreddit_slug):
    subreddit = get_object_or_404(Subreddit, id=subreddit_id)
    threads = Thread.objects.filter(subreddit=subreddit)
    return render(request, 'thread_list.html', {'subreddits': Subreddit.objects.all(),
                                                'current_subreddit': subreddit,
                                                'threads': threads})


def show_thread(request, subreddit_id, subreddit_slug, thread_id, thread_slug, comment_id=None):
    thread = get_object_or_404(Thread, id=thread_id)
    subreddit = get_object_or_404(Subreddit, id=subreddit_id)
    if comment_id:
        root_comment = get_object_or_404(Comment, id=comment_id)
        top_comment_level = len(root_comment.get_ancestors()) + MAX_COMMENT_LEVEL
    else:
        top_comment_level = MAX_COMMENT_LEVEL

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
        template_params = {'subreddits': Subreddit.objects.all(),
                           'current_subreddit': subreddit,
                           'thread': thread,
                           'nodes': Comment.objects.all(),
                           'comment_level': top_comment_level,
                           'max_level': MAX_COMMENT_LEVEL}
        if comment_id:
            template_params['root_comment'] = root_comment
        return render(request, 'thread.html', template_params)


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

def vote(request, entity_type, entity_id):
    is_next_up = False
    if request.method == 'POST':
        entity = get_object_or_404(entity_type, id=entity_id)
        if request.user in entity.voters.all():
            entity.voters.remove(request.user)
            is_next_up = True
        else:
            entity.voters.add(request.user)
            is_next_up = False
        entity.save()

    return JsonResponse({'votes': entity.voters.all().count(), 'next_up': is_next_up})

@login_required
def vote_on_comment(request, subreddit_id, subreddit_slug, thread_id, thread_slug, comment_id):
    return vote(request, Comment, comment_id)

@login_required
def vote_on_thread(request, subreddit_id, subreddit_slug, thread_id, thread_slug):
    return vote(request, Thread, thread_id)
