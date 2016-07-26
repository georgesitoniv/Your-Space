from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from braces.views import AnonymousRequiredMixin

from .forms import LogInForm, UserRegistrationForm, UserEditForm, ProfileEditForm, PasswordChangeForm
from .models import Profile
from post.models import Post


class LogIn(AnonymousRequiredMixin, View):

    """
        Log in view. Uses anonymous required mixin to prevent the user to access this view when logged in
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
                    
                else:
                    message.error(request,"Account Disabled")

        context = {
            'form': form
        }

        return HttpResponseRedirect(reverse_lazy("account:timeline"))

@login_required
def timeline(request, template="account/timeline.html", page_template="post/post.html"):
    """
        Timeline view. Contains post by followed users
    """   
    post = Post.objects.filter(user__in = request.user.profile.get_timeline_users()).order_by("-date_updated")

    context = {
        'posts' : post,
        'page_template':page_template,        
    }

    if request.is_ajax():
        template = page_template

    return render(request, template, context)
    

@login_required
def timeline_paginated(request):
 
    """
        Paginated Timeline view. Contains post by followed users
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
        Profile view. Let's the logged user to see his own profile and profile of other users
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
    """
         A view that displays all users
    """ 
    users = User.objects.all()

    context = {
        'users' : users,
    }

    return render(request, 'account/user_list.html', context)
    

class RegisterForm(View):
    """
        Register view. This view UserRegistrationForm and allows users to register.
    """ 
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

        context = {
            'user_form': user_form,
        }

        return render(request, self.template, context)





class ProfileEdit(View):
    """
      This view lets users to edit their information and profile. It uses two forms which are
      UserEditForm and ProfileEditForm
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
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        password_form = PasswordChangeForm()
        if "account_update_button" in request.POST:        
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Account information updated successfully')
            else:
                messages.error(request, 'Error in updating your account info')
        if "password_update_button" in request.POST:
            password_form = PasswordChangeForm(data=request.POST)
            if password_form.is_valid():
                cd = password_form.cleaned_data
                request.user.set_password(cd['new_password']) 
                request.user.save()
                request.user.is_authenticated = False    
                self.template = "registration/password_change_done.html"

                  
        context = {
            'user_form' : user_form,
            'profile_form' : profile_form,
            'password_form':password_form,
        }

        return render(request, self.template, context)

