from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.posts, name='posts'),
    url(r'^u/(?P<username>\w+)/$', views.user_view, name='user_view'),
    url(r'^p/(?P<username>\w+)/$', views.user_profile, name='user_profile'),
    url(r'^f/(?P<followee>\w+)/$', views.follow_user, name='follow_user'),
    url(r'^uf/(?P<followee>\w+)/$', views.unfollow_user, name='unfollow_user'),
    url(r'^comment/(?P<username>\w+)$', views.post_comment, name='post_comment'),
]
