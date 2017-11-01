# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .forms import signupForm, loginForm
from django.contrib.auth.hashers import make_password, check_password
from .models import User


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
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    print 'User is Valid'
                else:
                    print 'User invalid'


    elif request.method == 'GET':
        form = loginForm()

    return render(request, 'login.html', {'form': form})
