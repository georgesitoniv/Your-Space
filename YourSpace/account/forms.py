from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LogInForm(forms.Form):
    """
        Form for logging in
    """
    username = forms.CharField(max_length = 20)
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    """
        Registers the user.
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_validate = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email')
    
    def clean_username(self):
        cd = self.cleaned_data
        for char in cd['username']:
            print(char)
            if char == " ":
                raise forms.ValidationError("Please dont use spaces")
        return cd['username']

    def clean_password_validate(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_validate']:
            raise forms.ValidationError("Passwords does not match")
        return cd['password_validate']


class PasswordChangeForm(forms.Form):
    """
        Form that changes the user's password.
    """
    
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    validate_new_password = forms.CharField(label="Repeat New Password", widget=forms.PasswordInput)

    def clean_validate_new_password(self):
        cd = self.cleaned_data
        if cd['new_password'] != cd['validate_new_password']:
            raise forms.ValidationError("Password does not match")
        return cd['validate_new_password']

class UserEditForm(forms.ModelForm):

    """
        Form that will enable the user to edit his information
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):

    """
        Form that will enable the user to edit his profile
    """
    
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo','description')
        widgets = {
            'date_of_birth' :forms.DateInput,
            'description':forms.Textarea(attrs={
                'cols':30,
                'rows':4,
                'style':'resize:none'
                }),
        }
