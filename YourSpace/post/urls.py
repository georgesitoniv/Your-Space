from django.conf.urls import url, include
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    url(r'^create-post/$', views.create_post, name='create_post'),
    url(r'^(?P<id>[0-9]{1,10})/$', views.post_instance, name='post_instance'),
    url(r'^edit/(?P<id>[0-9]{1,10})/$', views.edit_post, name='edit_post'),
]
