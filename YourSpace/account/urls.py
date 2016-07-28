from django.conf.urls import url, include
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    url(r'^login/$', views.LogIn.as_view(), name='login'),
    url(r'^logout/$', views.LogOut.as_view(), name='logout'),
    url(r'^register/$', views.RegisterForm.as_view(), name='register'),
    url(r'^logout-then-login/$', auth_view.logout_then_login,name='logout_then_login'),
    url(r'^$', views.timeline_paginated, name='timeline'),
    url(r'^profile/(?P<username>[a-zA-z0-9_@+]{1,40})/$', views.profile, name='profile'),
    url(r'^edit-profile/$', views.ProfileEdit.as_view(), name='edit_profile'),
    url(r'^user-list/$', views.user_list, name='user_list'),
]
