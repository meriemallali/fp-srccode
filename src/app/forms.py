from django import forms
from .models import *
from django.contrib.auth.models import User


# save new user.
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


# update user profile.
class ProfileSettings(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


# create a new project
class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectManagement
        fields = ['project_name', 'description', 'team']



