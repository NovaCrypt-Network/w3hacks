from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from app import models
from home import models as homeModels
from datetime import datetime, date
import json


def generate_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])

def handler404(request, *args, **argv):
    return render(request, "errors/404.html")

def handler500(request, *args, **argv):
    return render(request, "errors/500.html")


def index(request):
    return HttpResponseRedirect("/dashboard/")

@login_required(login_url="/login/")
def dashboard(request):
    updates = homeModels.NewsUpdate.objects.all().order_by('-date_posted')

    upcoming_events = homeModels.Event.objects.all().order_by("-datetime")

    return render(request, "app/dashboard.html", context={
        "updates": updates,
        "upcoming_events": upcoming_events
    })


def user_login(request):
    next_url = request.GET.get("next")
    if request.user.is_authenticated:
        return HttpResponseRedirect("/dashboard/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticating user
        user = authenticate(username=username, password=password)

        if user: # Valid credentials
            if user.is_active: # User is active
                # Log the user in
                login(request, user)

                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect("/dashboard/")

            else: # User has an inactive account
                # Re-render page with error message
                return render(request, "app/login.html", context={
                    "message": "User account has been deactivated. Please sign up again.",
                    "status": "bad"
                })

        else: # Invalid credentials
            # Re-render page with error message
            return render(request, "app/login.html", context={
                "message": "Invalid credentials.",
                "status": "bad"
            })

    return render(request, "app/login.html")

@csrf_exempt
def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/dashboard/")

    if request.method == "POST":
        # Grabbing all pieces of form POST data
        # Grabbing default Django User data
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if username/email is used
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            return render(request, "app/sign-up.html", context={
                "message": "Username and/or email is already taken. Please double check.",
                "status": "bad"
            })


        # Creating the user
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )

        # Validate password
        try:
            validate_password(password, user)
        except ValidationError as e:
            return render(request, "app/sign-up.html", context={
                "errors": e
            })

        user.set_password(password) # Setting the password separately for encryption

        # Creating the custom profile
        profile = models.Profile(user=user)

        # Only save models when no errors have blocked registration
        user.save()
        profile.save()

        login(request, user) # Logging the user in

        return HttpResponseRedirect("/")

    return render(request, "app/sign-up.html")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("https://w3hacks.com/")


@login_required(login_url="/login/")
def leaderboards(request):
    profiles = models.Profile.objects.all().order_by("-ranking_points")

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Leaderboards", "link": "/leaderboards/"}
    ]

    return render(request, "app/leaderboards.html", context={
        "profiles": profiles,
        "breadcrumbs": breadcrumbs
    })


# Activities views
@login_required(login_url="/login/")
def exercises(request):
    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/"}
    ]

    return render(request, "app/exercises/exercises.html", context={
        "breadcrumbs": breadcrumbs
    })
