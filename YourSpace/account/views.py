from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from braces.views import AnonymousRequiredMixin, LoginRequiredMixin
from .forms import LogInForm, UserRegistrationForm, UserEditForm, ProfileEditForm, PasswordChangeForm
from .models import Profile
from post.models import Post


class LogIn(AnonymousRequiredMixin, View):
    """
    Returns a view containing a form for 
    user login if the user is anonymous.
    """
    template = "registration/login.html"

    def get(self, request):
        form = LogInForm()
        context = {
            'form': form
        }
        return render(request, self.template, context)

    def post(self, request):
        form = LogInForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse_lazy("account:timeline"))
                else:
                    message.error(request,"Account Disabled")
            else:
                messages.error(request, "Invalid Username or Password")
        context = {
            'form': form
        }
        return render(request, self.template, context)

class LogOut(View):
    def get(self, request):
        """Redirects to the timeline view if accessed via url."""
        return HttpResponseRedirect(reverse_lazy('account:timeline'))

    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('account:login'))

@login_required
def timeline_paginated(request):
    """
    Filters post by posts by followed users and posts by logged-in user
    and returns a view containing those posts.
    """
    if not Profile.objects.filter(user=request.user):
        profile = Profile.objects.create(user=request.user)

    post_list = Post.objects.filter(user__in = request.user.profile.get_timeline_users()).order_by("-date_updated")

    if request.method == "POST":
        if "sortByOldest_button" in request.POST:
            post_list = post_list.order_by("date_updated")
        if "sortByPopularity_button" in request.POST:
            post_list = post_list.annotate(num_likes=Count("likes")).order_by("-num_likes")

    paginator = Paginator(post_list, 15)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts' : posts,
        'post_count':post_list.count,
    }

    return render(request, 'account/timeline.html', context)

@login_required
def profile(request, username='test'):
    """
    Returns a view containing a user's profile, posts, followers, and, followed users.
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("Error")

    if request.method == "POST":
        if "follow_button" in request.POST:
            request.user.profile.follow.add(user.profile)
        if "unfollow_button" in request.POST:
            request.user.profile.follow.remove(user.profile)
    
    post_list = user.post_set.all().order_by("-date_updated","-likes")
    paginator = Paginator(post_list, 10)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)    

    context = {
        'user': user, 
        'posts': posts,
        'follows' : request.user.profile.is_following(user),
        'post_count':post_list.count,
             
    }

    return render(request, 'account/profile.html', context)

def user_list(request):
    """Returns a view containing all registered users."""
    users = User.objects.all()
    context = {
        'users' : users,
    }
    return render(request, 'account/user_list.html', context)

class RegisterForm(View):
    template = "account/register.html"

    def get(self, request):
        user_form = UserRegistrationForm()
        context={
            'user_form':user_form,
        }       
        return render(request, self.template, context)

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            messages.success(request, "You have successfully registered")
            user_form = UserRegistrationForm()
        else:
            messages.error(request, "Please review the field errors, make sure each field contains valid characters and please do not add trailing whitespaces")    
        context = {
            'user_form': user_form,
        }
        return render(request, self.template, context)

class ProfileEdit(LoginRequiredMixin,View):
    """
    Returns a view containing three forms. 
    UserEditForm and ProfileEditForm was implemented to
    edit a user's information. While, PasswordChangeForm
    was implemented to change the user's password
    """
    template = 'account/edit_profile.html'

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        password_form = PasswordChangeForm()
        context = {
            'user_form' : user_form,
            'profile_form' : profile_form,
            'password_form':password_form,
        }  
        return render(request, self.template, context)

    def post(self, request):   
        if "account_update_button" in request.POST:
            user_form = UserEditForm(instance=request.user, data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
            password_form = PasswordChangeForm()      
            if user_form.is_valid() and profile_form.is_valid():
                if request.user.profile.email_validate(user_form.cleaned_data['email']):
                    user_form.save()
                    profile_form.save()
                    messages.success(request, 'Account information updated successfully')
                else:
                    messages.error(request, 'Email already used.')
            else:
                messages.error(request, "Please make sure each field contains valid characters and please do not add trailing whitespaces")
        elif "password_update_button" in request.POST:
            """Changes the user's password and will end the session if the form is valid."""                          
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
            password_form = PasswordChangeForm(data=request.POST)
            if password_form.is_valid():
                cd = password_form.cleaned_data
                request.user.set_password(cd['new_password']) 
                request.user.save()
                logout(request)    
                self.template = "registration/password_change_done.html"
            else:
                messages.error(request, "Please make sure each field contains valid characters and please do not add trailing whitespaces")

        context = {
            'user_form' : user_form,
            'profile_form' : profile_form,
            'password_form':password_form,
        }

        return render(request, self.template, context)