from django.shortcuts import render
from django.utils import timezone
from .models import Post

# Create your views here.
def posts(request):
    posts = Post.objects.all().order_by('created_date')
    return render(request, 'waffle/list_all_posts.html', {'posts': posts})


def user_view(request, username):
    thisuser='richard'
    posts = Post.objects.filter(author=username)
    return render(request, 'waffle/list_all_posts.html', {'posts': posts})
