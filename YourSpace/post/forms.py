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

    def clean_content(self):
        cd = self.cleaned_data
        if cd['content'] is None:
            raise forms.ValidationError("Please provide a comment")
        return cd['content']     
