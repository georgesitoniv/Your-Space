from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect


from .models import Post, PostComments
from .forms import PostForm, CommentForm

@login_required
def create_post(request):

    template = "post/create_post.html"   
    post_form = PostForm()


    if request.method == "POST":
        if "post_button" in request.POST:   
            post_form = PostForm(data=request.POST, files=request.FILES)
            if post_form.is_valid():
                post_form = post_form.save(commit=False)
                if post_form.content or post_form.image:
                        post_form.user = request.user
                        post_form.save()
                        messages.success(request, "Post Successfully Created")
                        post_form = PostForm()
                else:
                    post_form = PostForm()
                    messages.error(request, "Empty posts are restricted")



        
    context = {
        'post_form':post_form,
        'page_title':'Create a Post',  
    }

    return render(request, template, context)

@login_required
def edit_post(request, id = '1'):
    template = "post/create_post.html"
    post = Post.objects.get(id=id)
    post_form = PostForm(instance = post)

    if not request.user.username == post.user.username:
        messages.error(request,"You can not edit posts by other users")
        return HttpResponseRedirect(reverse_lazy('post:create_post'))

    if request.method == "POST":
        if "post_button" in request.POST:   
            post_form = PostForm(instance = post, data=request.POST, files=request.FILES)
            if post_form.is_valid():
                post_form = post_form.save(commit=False)
                if post_form.content or post_form.image:
                    post_form.user = request.user
                    post_form.save()
                    post_form = PostForm(instance = post)
                    messages.success(request, "Post Successfully Edited")
                else:
                    post_form = PostForm()
                    messages.error(request, "Empty posts are restricted")
                    
        elif "remove_post_button" in request.POST:
            user = post.user
            post.delete()
            messages.success(request, "Post successfully deleted")
            return HttpResponseRedirect(reverse_lazy('account:profile',kwargs={'username':user.username}))
           
        else:
            pass
        
    context = {
        'post_form':post_form,
        'page_title':'Edit Post',
        'post': post,
    }

    return render(request, template, context)

@login_required
def post_instance(request, id = '1'):
    template = "post/post_instance.html"
    post = Post.objects.get(id=id)
    comment_form = CommentForm()
    try:    
        comments = post.postcomments_set.all()

    except PostComments.DoesNotExist():
        comments = None


    if request.method == "POST":
        if "like_button" in request.POST:
            if post.has_liked(request.user):
                post.likes.remove(request.user)                
            else:
                post.likes.add(request.user)   
            
        elif "unlike_button" in request.POST:
            post.likes.remove(request.user)

        elif "comment_button" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid:
                comment_form = comment_form.save(commit = False)
                comment_form.user = request.user
                comment_form.post = post
                comment_form.save()
            comment_form = CommentForm()
 
        else:
            pass

    context = {
        'post': post,
        'has_liked':post.has_liked(request.user),
        'view':True,
        'comment_form':comment_form,
        'comments':comments,
    }

    return render(request, template, context)
    
