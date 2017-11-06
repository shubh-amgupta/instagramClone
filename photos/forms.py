from django import forms
from models import User, PostModel


class signupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'password', 'email']



class loginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class postForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['image', 'caption']