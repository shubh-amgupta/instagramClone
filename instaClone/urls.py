"""instaClone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from photos.views import signup,login, post, feed, like, comment, logout, search_user, upvote

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login),
    url(r'^post/', post),
    url(r'^feed/', feed),
    url(r'^post/feed', feed),
    url(r'^like/', like),
    url(r'^comment/', comment),
    url(r'^logout/', logout),
    url(r'^search/', search_user),
    url(r'^upvote/', upvote),
    url(r'^$', signup),
]
