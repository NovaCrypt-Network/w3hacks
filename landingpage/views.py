from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.core.mail.message import EmailMessage
from django.db import IntegrityError
from main import models
from datetime import date, datetime
import random
import string


def generate_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])


def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email_body = f"From: {name}\nEmail: {email}\n\n{message}"
        EmailMessage("w3Hacks Contact Us", email_body, to=["calix.huang1@gmail.com"]).send()

        return render(request, "landingpage/index.html", context={
            "message": "Message sent!"
        })

    return render(request, "landingpage/index.html")


def about(request):
    return render(request, "landingpage/about.html")


def contact(request):
    return render(request, "landingpage/contact.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticating user
        user = authenticate(username=username, password=password)

        if user: # Valid credentials
            if user.is_active: # User is active
                # Log the user in
                login(request, user)
                return HttpResponseRedirect("http://app.w3hacks.com") # Redirect to App

            else: # User has an inactive account
                # Re-render page with error message
                return render(request, "landingpage/login.html", context={
                    "message": "User account has been deactivated. Please register again.",
                    "status": "bad"
                })

        else: # Invalid credentials
            # Re-render page with error message
            return render(request, "landingpage/login.html", context={
                "message": "Invalid credentials.",
                "status": "bad"
            })

    return render(request, "landingpage/login.html")


def register(request):
    if request.method == "POST":
        # Grabbing all pieces of form POST data
        # Grabbing default Django User data
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # # Grabbing custom profile data
        # biography = request.POST.get("biography")
        # birthday = request.POST.get("birthday")
        # education = request.POST.get("education")
        # skills = request.POST.get("skills").split(",")
        #
        # # Social Links
        # github_profile = request.POST.get("github-profile")
        # linkedin_profile = request.POST.get("linkedin-profile")
        # twitter_profile = request.POST.get("twitter-profile")
        # instagram_profile = request.POST.get("instagram-profile")
        # facebook_profile = request.POST.get("facebook-profile")
        # twitch_profile = request.POST.get("twitch-profile")
        # personal_website = request.POST.get("personal-website")

        # Creating the user
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )
        user.set_password(password) # Setting the password separately for encryption

        # Creating the custom profile
        profile = models.Profile(
            user=user,
            # biography=biography,
            # education=education,
            # skills=skills,
            # github_profile=github_profile,
            # linkedin_profile=linkedin_profile,
            # twitter_profile=twitter_profile,
            # instagram_profile=instagram_profile,
            # facebook_profile=facebook_profile,
            # twitch_profile=twitch_profile,
            # personal_website=personal_website
        )

        # # To avoid 'Invalid Date Format' error for empty birthday
        # if birthday:
        #     profile.birthday = birthday

        # # Checking if they provided picture
        # if 'profile-picture' in request.FILES:
        #     profile.profile_picture = request.FILES['profile-picture']


        # Only save models when no errors have blocked registration
        try:
            user.save()
            profile.save()
        except IntegrityError:
            return render(request, "landingpage/register.html", context={
                "message": "Username and/or email is already taken. Please double check.",
                "status": "bad",
                "today": str(date.today())
            })


        login(request, user) # Logging the user in

        return HttpResponseRedirect("http://app.w3hacks.com")

    return render(request, "landingpage/register.html", context={
        "today": str(date.today())
    })
