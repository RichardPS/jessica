from django.shortcuts import render
from django.db.models.expressions import Value
from django.db import models

from .models import Post


def posts(request):
    allposts = Post.objects.all().order_by('created_date')
    return render(
        request,
        'waffle/list_all_posts.html',
        {'allposts': allposts}
        )


def user_view(request, username):
    posts = Post.objects.filter(
        author__username=username
        ).annotate(
        is_repost=Value(
            0, models.IntegerField()
            )
        )

    reposted = Post.objects.filter(
        repost__reposter__username=username
        ).annotate(
        is_repost=Value(
            1, models.IntegerField()
            )
        )

    allposts = posts.union(reposted).order_by('created_date')

    # import pdb; pdb.set_trace()

    return render(
        request,
        'waffle/list_all_posts.html',
        {'allposts': allposts}
        )


def user_profile(request, username):
    return render(request, 'waffle/view_profile.html', {})
