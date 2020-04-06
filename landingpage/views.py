from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from main import models
from datetime import date

def index(request):
    return render(request, "landingpage/index.html", context={"auth": request.user.is_authenticated})


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
                return HttpResponse("User account has been deactivated. Please register again.")

        else: # Invalid credentials
            return HttpResponse("Invalid credentials.")

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

        # Grabbing custom profile data
        biography = request.POST.get("biography")
        birthday = request.POST.get("birthday")
        education = request.POST.get("education")
        profile_picture = request.FILES["profile-picture"]
        skills = request.POST.get("skills").split(",")

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
            biography=biography,
            education=education,
            skills=skills
        )

        # To avoid 'Invalid Date Format' error for empty birthday
        if birthday:
            profile.birthday = birthday

        # Checking if they provided picture
        if 'profile-picture' in request.FILES:
            profile.profile_picture = request.FILES['profile-picture']


        # Only save models when no errors have blocked registration
        user.save()
        profile.save()


        login(request, user) # Logging the user in

        return HttpResponseRedirect("http://app.w3hacks.com")

    print(str(date.today()))
    return render(request, "landingpage/register.html", context={
        "today": str(date.today())
    })
