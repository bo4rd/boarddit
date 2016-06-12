from django.shortcuts import render, get_object_or_404
from .models import Thread, Comment

def index(request):
    return render(request, 'index.html', {'threads': Thread.objects.all()})

def show_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    return render(request, 'thread.html', {'thread': thread,
                                           'nodes': Comment.objects.all()})
