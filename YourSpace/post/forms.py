from django import forms
from django.contrib.auth.models import User

from post.models import Post, PostComments


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('image','content')
        widgets = {
            'content':forms.Textarea(attrs={
                'cols':42,
                'rows':4,
                'style':'resize:none'
                }),
        }

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = PostComments
        fields = ('content',)
        widgets = {
            'content':forms.Textarea(attrs={
                'cols':35,
                'rows':4,
                'style':'resize:none'
                }),
        }
