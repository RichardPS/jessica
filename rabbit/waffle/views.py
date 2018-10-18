from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.expressions import Value
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models

import pdb

from .forms import CommentForm
from .models import Post
from .models import Comment
from .models import Follow
from . import settings


def posts(request):
    allposts = Post.objects.all().order_by('created_date')
    return render(
        request,
        'waffle/list_all_posts.html',
        {'allposts': allposts}
        )


def single_post(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post__pk=pk).order_by('comment_date')

    # pdb.set_trace()

    return render(
        request,
        'waffle/list_single_post.html',
        { 'post': post, 'comments': comments }
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

    # pdb.set_trace()

    return render(
        request,
        'waffle/list_all_posts.html',
        {'allposts': allposts}
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
        {
            'user_profile': user_profile,
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
        messages.success(
            request,
            settings.FOLLOW_USER_SUCCESS_MESSAGE.format(followee)
            )
    else:
        return redirect('/p/' + followee)

    return redirect('/p/' + followee)


def unfollow_user(request, followee):
    if request.method == 'POST':
        followee_user = User.objects.get(username=followee)
        following_user = request.user
        unfollow = Follow.objects.filter(
            follower=following_user,
            followee=followee_user
            )

        for follows in unfollow:
            follows.delete()

        messages.success(
            request,
            settings.UNFOLLOW_USER_SUCCESS_MESSAGE.format(followee)
            )
    else:
        return redirect('/p/' + followee)

    return redirect('/p/' + followee)


def post_comment(request, pk):
    user = request.user
    post = get_object_or_404(Post, pk=int(pk))

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commenter = user
            comment.post = post

            comment.save()

    messages.success(
        request,
        settings.POST_COMMENT_SUCCESS_MESSAGE.format(post.author.username)
        )
    # pdb.set_trace()
    return redirect('/u/' + post.author.username)
