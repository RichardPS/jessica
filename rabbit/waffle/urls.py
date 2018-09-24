from django.conf.urls import url
import re

from . import views

urlpatterns = [
    url(r'^$', views.posts, name='posts'),
    url(r'^u/(?P<username>\w+)/$', views.user_view, name='user_view'),
]
