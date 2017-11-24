from django import forms
from models import User, PostModel, LikeModel, CommentModel


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


class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields = ['post']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post']