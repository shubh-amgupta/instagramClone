# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
import uuid


class User(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=400)
    email = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username + ' (' + self.email + ') '


class SessionToken(models.Model):
    user = models.ForeignKey(User)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def createToken(self):
        self.session_token = uuid.uuid4()


class PostModel(models.Model):
    user = models.ForeignKey(User)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # def __init__(self, image=None, image_url=None, caption=None, *args, **kwargs):
    #     super(PostModel, self).__init__(*args, **kwargs)
    #     self.image = image or self.image
    #     self.image_url = image_url or self.image_url
    #     self.caption = caption or self.caption
