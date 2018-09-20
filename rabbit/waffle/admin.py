from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Repost, Follow 

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Repost)
admin.site.register(Follow)
