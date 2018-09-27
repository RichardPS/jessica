from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.posts, name='posts'),
    url(r'^u/(?P<username>\w+)/$', views.user_view, name='user_view'),
    url(r'^p/(?P<username>\w+)/$', views.user_profile, name='user_profile'),
]
