# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import signupForm, loginForm, postForm
from django.contrib.auth.hashers import make_password, check_password
from .models import User, SessionToken, PostModel, LikeModel
from imgurpython import ImgurClient
from instaClone.settings import BASE_DIR


CLIENT_ID = '27e5c7f70526d0e'
CLIENT_SECRET = '46083ca5c1ed6e35dcad9176a608e9aee9df915a'


# Create your views here.


def signup(request):
    if request.method == "POST":
        form = signupForm(request.POST)  # if post request is received pass the data into signupForm class
        if form.is_valid():  # if form data is valid django validates data.
            username = form.cleaned_data['username']  # extractiong cleaned data. Automatically done in new python and django versions
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving user to database
            user = User(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'login.html')

    elif request.method == 'GET':
        form = signupForm()  # if form request is post resturn empty form

    return render(request, 'index.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form:
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.createToken()
                    token.save()
                    response = redirect('/feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    return render(request, 'index.html')
        else:
            print "Nothing is obtained ----- 2"

    elif request.method == 'GET':
        form = loginForm()

    return render(request, 'login.html', {'form': form})


def checkValidation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user

    else:
        return None


def post(request):
    user = checkValidation(request)

    if user:
        if request.method == 'GET':
            form = postForm()

        elif request.method == 'POST':
            form = postForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                postimage = PostModel(user=user, image=image, caption=caption)
                postimage.save()
                path = str(BASE_DIR + '/' + postimage.image.url)
                client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
                postimage.image_url = client.upload_from_path(path, anon=True)['link']
                postimage.save()
                return HttpResponseRedirect('feed.html')

        return render(request, 'upload.html', {'form': form})
    else:
        return redirect('/login/')


def feed(request):
    user = checkValidation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')


def like(request):
    user = checkValidation(request)

    if user and request.method == 'POST':
        form = like(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()

            return redirect('/feed/')
    else:
        return redirect('/login/')

