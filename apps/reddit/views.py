from django.shortcuts import render
from .models import Thread, Comment

def index(request):
    return render(request, 'index.html', {'threads': Thread.objects.all(),
                                          'nodes': Comment.objects.all()})
