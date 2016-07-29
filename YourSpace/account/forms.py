from django import forms
from django.forms import FileField, ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .models import Profile


class LogInForm(forms.Form):
    username = forms.CharField(max_length="40")
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    alpanumeric = RegexValidator(regex="^[a-zA-Z0-9]*$", message="Please use alpanumeric characters only")
    name = RegexValidator(regex="^[a-zA-Z ]*$", message="Please enter a valid name")
    username = forms.CharField(label="Username", min_length="6", max_length="40", required = True, validators=[alpanumeric,])
    first_name = forms.CharField(label="First Name", max_length="50", required = True, validators=[name,])
    last_name = forms.CharField(label="Last Name", max_length="50", required = True, validators=[name,])
    password = forms.CharField(label='Password', min_length="6", widget=forms.PasswordInput)
    password_validate = forms.CharField(label='Repeat Password',min_length="6", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')
    
    def clean_email(self):
        """Raises a validation error if email is already used or left blank."""
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("Email is required")
        elif User.objects.filter(email=email):
            raise forms.ValidationError("Email is already used.")
        return email

    def clean_password_validate(self):
        cd = self.cleaned_data
        try:
            if cd['password'] != cd['password_validate']:
                raise forms.ValidationError("Passwords does not match")
        except KeyError:
            raise forms.ValidationError("Password is required")          
        return cd['password_validate']

    def clean(self):
        """Raises a validation error when any form data contain's trailing whitespaces.'"""
        cd = self.cleaned_data
        for field in cd:
            if cd[field] != cd[field].strip():
                raise forms.ValidationError("There are trailing whitespaces")


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    validate_new_password = forms.CharField(label="Repeat New Password", widget=forms.PasswordInput)

    def clean_validate_new_password(self):
        cd = self.cleaned_data
        try:
            if cd['new_password'] != cd['validate_new_password']:
                raise forms.ValidationError("Password does not match")
        except KeyError:
            raise forms.ValidationError("Password is required") 
        return cd['validate_new_password']

class UserEditForm(forms.ModelForm):
    name = RegexValidator(regex="^[a-zA-Z ]*$", message="Please enter a valid name")
    first_name = forms.CharField(label="First Name", max_length="50", required = True, validators=[name,])
    last_name = forms.CharField(label="Last Name", max_length="50", required = True, validators=[name,])
    email = forms.CharField(label="Email", max_length="50", required = True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean(self):
        """Raises a validation error when any form data contain's trailing whitespaces.'"""
        cd = self.cleaned_data
        for field in cd:
            if cd[field] != cd[field].strip():
                raise forms.ValidationError("There are trailing whitespaces")

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo','description')
        widgets = {
            'date_of_birth' :forms.DateInput,
            'description':forms.Textarea(attrs={
                'cols':40,
                'rows':4,
                'style':'resize:none'
                }),
        }