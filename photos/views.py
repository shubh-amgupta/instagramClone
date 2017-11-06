# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import signupForm, loginForm, postForm
from django.contrib.auth.hashers import make_password, check_password
from .models import User, SessionToken


# Create your views here.


def signup(request):
    if request.method == "POST":
        form = signupForm(request.POST)  # if post request is received pass the data into signupForm class
        if form.is_valid():  # if form data is valid django validates data.
            username = form.cleaned_data[
                'username']  # extractiong cleaned data. Automatically done in new python and django versions
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving user to database
            user = User(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html')

    elif request.method == 'GET':
        form = signupForm()  # if form request is post resturn empty form

    return render(request, 'index.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        print form
        if form:
            username = request.POST['username']
            password = form.cleaned_data['password']
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

                postimage = postForm(user=user, image=image, caption=caption)
                postimage.save()
                return HttpResponse("Post uploaded!")

        return render(request, 'upload.html', {'form': form})
    else:
        return redirect('/login/')


def feed(request):
    return render(request, 'success.html')
