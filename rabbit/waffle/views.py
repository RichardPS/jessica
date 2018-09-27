from django.shortcuts import render
from .models import Post
from .models import Repost


def posts(request):
    posts = Post.objects.all().order_by('created_date')
    return render(request, 'waffle/list_all_posts.html', {'posts': posts})


def user_view(request, username):
    posts = Post.objects.filter(
        author__username=username
        ).order_by('created_date')


    reposted = Repost.objects.filter(
        reposter__username=username
        )


    return render(
        request,
        'waffle/list_all_posts.html',
        {'posts': posts, 'reposted': reposted}
        )
