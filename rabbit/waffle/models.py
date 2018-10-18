from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{0}: {1}'.format(self.author, self.id)

    def get_absolute_url(self):
        return '/sp/{0}'.format(self.author.pk)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    comment = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{0}: {1}'.format(self.commenter, self.id)


class Repost(models.Model):
    reposter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        on_delete=models.CASCADE
        )
    followee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followees',
        on_delete=models.CASCADE
        )

    def __str__(self):
        return '{0} follows: {1}'.format(self.follower, self.followee)


class Mention(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='mentions',
        on_delete=models.CASCADE
        )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
