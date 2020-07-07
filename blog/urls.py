from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
from . import views as views
from hackathon import views as hackathonViews

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^blog/(?P<blog_url>[^/]+)$", views.post, name="post"),
]
