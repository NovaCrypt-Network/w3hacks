from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, date
from . import models


@login_required(login_url="/login/")
def profile(request, username):
    # Getting current user
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        return render(request, "errors/user-does-not-exist.html")

    # Getting profile from current user
    profile = models.Profile.objects.get(user=user)

    # Grabbing all past hackathons for current user
    past_hackathons = list(profile.past_hackathons.all())

    # Grabbing all completed exercises
    completed_project_exercises = list(profile.completed_project_exercises.all())
    completed_quiz_exercises = list(profile.completed_quiz_exercises.all())

    return render(request, "app/profile.html", context={
        "profile": profile,
        "past_hackathons": past_hackathons,
        "completed_project_exercises": completed_project_exercises,
        "completed_quiz_exercises": completed_quiz_exercises,
    })


@login_required(login_url="/login/")
def edit_profile(request, username):
    # Getting current user
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        return render(request, "errors/does-not-exist", context={
            "title": "User doesn't exist!",
            "content": "We're sorry, but we couldn't find the user you were looking for! That user has either been removed, or never existed in the first place. Please go back to the previous page if possible."
        })

    # Getting profile from current user
    profile = models.Profile.objects.get(user=user)

    # Checking to see if current user is the one editing profile
    if user != request.user:
        return render(request, "errors/does-not-exist.html", context={
            "title": "Permission Error",
            "content": "We're sorry, but you don't have permission to modify this profile. Only the logged in user of this account has permission to modify any of the content of their profile."
        })

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
        skills = request.POST.get("skills").split(",")

        # Social Links
        github_profile = request.POST.get("github-profile")
        linkedin_profile = request.POST.get("linkedin-profile")
        twitter_profile = request.POST.get("twitter-profile")
        instagram_profile = request.POST.get("instagram-profile")
        facebook_profile = request.POST.get("facebook-profile")
        twitch_profile = request.POST.get("twitch-profile")
        personal_website = request.POST.get("personal-website")

        # Check if username/email is used
        if (User.objects.filter(email=email).exists() and email != request.user.email) or (User.objects.filter(username=username).exists() and username != request.user.username):
            return render(request, "app/edit-profile.html", context={
                "message": "Username and/or email is already taken. Please double check.",
                "status": "bad",
                "profile": profile
            })

        # Updating user
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        # Updating profile
        profile = models.Profile.objects.get(user=request.user)
        profile.biography = biography
        profile.education = education
        profile.skills = skills
        profile.github_profile = github_profile
        profile.linkedin_profile = linkedin_profile
        profile.twitter_profile = twitter_profile
        profile.instagram_profile = instagram_profile
        profile.facebook_profile = facebook_profile
        profile.twitch_profile = twitch_profile
        profile.personal_website = personal_website

        # To avoid 'Invalid Date Format' error for empty birthday
        if birthday:
            profile.birthday = birthday

        # Checking if they provided picture
        if 'profile-picture' in request.FILES:
            profile.profile_picture = request.FILES['profile-picture']

        user.save()
        profile.save()

        return HttpResponseRedirect("/@" + user.username)

    return render(request, "app/edit-profile.html", context={ "profile": profile })
