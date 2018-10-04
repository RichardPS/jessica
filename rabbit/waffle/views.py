from django.shortcuts import render, redirect
from django.db.models.expressions import Value
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models

from .models import Post
from .models import Follow
from .forms import CommentForm

import pdb


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

    form = CommentForm()

    # pdb.set_trace()

    return render(
        request,
        'waffle/list_all_posts.html',
        {'allposts': allposts, 'form': form}
        )


def user_profile(request, username):
    user_profile = User.objects.get(username=username)
    followers = Follow.objects.filter(followee__username=username)
    following = Follow.objects.filter(follower__username=username)

    already_follows = Follow.objects.filter(
        followee__username=username
        ).filter(
        follower__username=request.user.username
        ).count()

    # pdb.set_trace()

    return render(
        request,
        'waffle/view_profile.html',
        {'user_profile': user_profile,
            'followers': followers,
            'following': following,
            'already_follows': already_follows,
            }
        )


def follow_user(request, followee):

    if request.method == 'POST':        
        followee_user = User.objects.get(username=followee)
        following_user = request.user
        Follow.objects.create(follower=following_user, followee=followee_user)
        messages.success(request, 'You are now following {0}'.format(followee))
    else:
        return redirect ('/p/' + followee)

    return redirect ('/p/' + followee)


def unfollow_user(request, followee):
    if request.method == 'POST':  
        followee_user = User.objects.get(username=followee)
        following_user = request.user
        unfollow = Follow.objects.filter(follower=following_user, followee=followee_user)

        for follows in unfollow:
            follows.delete()

        messages.success(request, 'You have now unfollowed {0}'.format(followee))
    else:
        return redirect ('/p/' + followee)


    return redirect ('/p/' + followee)
