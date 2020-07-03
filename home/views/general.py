from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from main import models
from datetime import datetime, date
import json


def generate_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])

def handler404(request, *args, **argv):
    return render(request, "errors/404.html")

def handler500(request, *args, **argv):
    return render(request, "errors/500.html")


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/dashboard/")

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email_body = f"From: {name}\nEmail: {email}\n\n{message}"
        EmailMessage("w3Hacks Contact Us", email_body, to=["calix.huang1@gmail.com"]).send()

        return render(request, "home/index.html", context={
            "message": "Message sent!"
        })

    return render(request, "landingpage/index.html")


def contact(request):
    return render(request, "landingpage/contact.html")


def user_login(request):
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
                return HttpResponseRedirect("/dashboard/")

            else: # User has an inactive account
                # Re-render page with error message
                return render(request, "home/login.html", context={
                    "message": "User account has been deactivated. Please register again.",
                    "status": "bad"
                })

        else: # Invalid credentials
            # Re-render page with error message
            return render(request, "home/login.html", context={
                "message": "Invalid credentials.",
                "status": "bad"
            })

    return render(request, "landingpage/login.html")


def register(request):
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

        # Creating the user
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )
        user.set_password(password) # Setting the password separately for encryption

        # Creating the custom profile
        profile = models.Profile(user=user)

        # Only save models when no errors have blocked registration
        try:
            user.save()
            profile.save()
        except IntegrityError:
            return render(request, "home/register.html", context={
                "message": "Username and/or email is already taken. Please double check.",
                "status": "bad"
            })


        login(request, user) # Logging the user in

        return HttpResponseRedirect("/")

    return render(request, "landingpage/register.html", context={
        "today": str(date.today())
    })


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "home/dashboard.html")


@login_required(login_url="/login/")
def leaderboards(request):
    all_profiles = models.Profile.objects.all()

    overall_rankings = sorted(all_profiles, key=lambda x: x.overall_ranking_points)
    project_rankings = sorted(all_profiles, key=lambda x: x.project_ranking_points)
    quiz_rankings = sorted(all_profiles, key=lambda x: x.quiz_ranking_points)
    exercise_rankings = sorted(all_profiles, key=lambda x: x.exercise_ranking_points)

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Leaderboards", "link": "/leaderboards/"}
    ]

    return render(request, "home/leaderboards.html", context={
        "overall_rankings": overall_rankings,
        "project_rankings": project_rankings,
        "quiz_rankings": quiz_rankings,
        "exercise_rankings": exercise_rankings,
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

    return render(request, "home/exercises/exercises.html", context={
        "breadcrumbs": breadcrumbs
    })


# Hackathon views
@login_required(login_url="/login/")
def about_the_hackathon(request):
    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "About The Hackathon", "link": "/about-the-hackathon/"}
    ]

    return render(request, "home/hackathon/about-the-hackathon.html", context={
        "breadcrumbs": breadcrumbs
    })


@login_required(login_url="/login/")
def past_hackathons(request):
    all_hackathons = models.Hackathon.objects.all()

    past_hackathons = []
    for hackathon in all_hackathons:
        # Hackathon end date was less than today
        if hackathon.end_datetime.strftime("%d/%m/%Y %H:%M:%S") < datetime.now().strftime("%d/%m/%Y %H:%M:%S"):
            past_hackathons.append(hackathon)

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Past Hackathons", "link": "/past-hackathons/"}
    ]

    return render(request, "home/hackathon/past-hackathons.html", context={
        "past_hackathons": past_hackathons,
        "breadcrumbs": breadcrumbs
    })


@login_required(login_url="/login/")
def future_hackathons(request):
    all_hackathons = models.Hackathon.objects.all()

    future_hackathons = []
    for hackathon in all_hackathons:
        # Hackathon end date was less than today
        if hackathon.start_datetime.strftime("%d/%m/%Y %H:%M:%S") > datetime.now().strftime("%d/%m/%Y %H:%M:%S"):
            future_hackathons.append(hackathon)

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Future Hackathons", "link": "/future-hackathons/"}
    ]

    return render(request, "home/hackathon/future-hackathons.html", context={
        "future_hackathons": future_hackathons,
        "breadcrumbs": breadcrumbs
    })
