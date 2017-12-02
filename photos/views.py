# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import signupForm, loginForm, postForm, LikeForm, CommentForm
from django.contrib.auth.hashers import make_password, check_password
from .models import User, SessionToken, PostModel, LikeModel, CommentModel
from imgurpython import ImgurClient
from instaClone.settings import BASE_DIR
from clarifai.rest import ClarifaiApp
import sendgrid
import os
from sendgrid.helpers.mail import *


SENDGRID_API_KEY = ""


CLIENT_ID = '27e5c7f70526d0e'
CLIENT_SECRET = '46083ca5c1ed6e35dcad9176a608e9aee9df915a'
API_KEY = 'ce04b125186749c59e20342e6b13719c'


# Create your views here.


def signup(request):
    logout(request)
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
    logout(request)
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


def getSessionID(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.session_token

    else:
        return None


checks = ['garbage', 'calamity', 'waste', 'pollution', 'trash']


def ifDirty(url):
    app = ClarifaiApp(api_key=API_KEY)

    # get the general model
    model = app.models.get("general-v1.3")

    # predict with the model
    result = model.predict_by_url(url=url)
    for i in result['outputs'][0]['data']['concepts']:
        if i['name'] in checks and i['value'] > 0.7:
            return True
            break


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
                dirty = ifDirty(postimage.image_url)
                postimage.save()
                if dirty:
                    postimage.ifdirty = True
                    postimage.save()

                return HttpResponseRedirect('../feed/')

        return render(request, 'upload.html', {'form': form})
    else:
        return redirect('/login/')


def feed(request):
    user = checkValidation(request)
    if user:
        posts = PostModel.objects.all().order_by('-created_on')
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html', {'posts': posts, 'user': user})
    else:
        return redirect('/login/')


def like(request):
    user = checkValidation(request)

    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            username = form.cleaned_data.get('post')
            useremail = User.objects.filter(username=username).first().email

            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
                #email
                sendmail(str(useremail), "InstaClone: Like on Post", "Some user have liked on your post")

            else:
                existing_like.delete()

            return redirect('/feed/')
    else:
        return redirect('/login/')


def comment(request):
    user = checkValidation(request)

    if user and request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            username = form.cleaned_data.get('post')
            useremail = User.objects.filter(username=username).first().email

            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            sendmail(str(useremail), "InstaClone: Comment on Post", "Some user have commented on your post")

            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login/')


def logout(request):
    if request.method == 'GET':
        user = checkValidation(request)

        if user:

            session = getSessionID(request)

            if session:
                username = SessionToken.objects.get(session_token=session)
                if username:
                    username.delete()
                    response = redirect('../')
                    return response


def search_user(request):
    user = checkValidation(request)
    if user:
        searchuser = request.POST['search']
        if searchuser == '':
            posts = PostModel.objects.all().order_by('-created_on')

        else:
            posts = PostModel.objects.all().filter(user=searchuser).order_by('-created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html', {'posts': posts, 'user': user})
    else:
        return redirect('/login/')


def upvote(request):
    user = checkValidation(request)

    if user and request.method == 'POST':
            comment_id = request.POST.get('comment')

            existing_vote = CommentModel.objects.filter(post_id=comment_id, user=user).first()

            if existing_vote:
                post = CommentModel.objects.filter(post=comment_id)
                post.votes = False

            else:
                post = CommentModel.objects.filter(post=comment_id)
                post.votes = True

            return redirect('/feed/')
    else:
        return redirect('/login/')


def sendmail(email, subj, cont):
    try:
        sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
        from_email = Email("instaacadview@gmail.com")
        to_email = Email(email)
        subject = subj
        content = Content("text/plain", cont)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception, e:
        print str(e) + "------exception------"
