from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from main import models

def index(request):
    return render(request, "landingpage/index.html")


def about(request):
    return render(request, "landingpage/about.html")


def contact(request):
    return render(request, "landingpage/contact.html")


def user_login(request):
    return render(request, "landingpage/login.html")


def register(request):
    return render(request, "landingpage/register.html")
