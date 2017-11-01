from django import forms
from models import User


class signupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'password', 'email']



class loginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']