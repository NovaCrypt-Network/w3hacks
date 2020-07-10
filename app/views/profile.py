from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, date
from app import models
import requests


@login_required(login_url="/login/")
def profile(request, username):
    # Getting current user
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        return render(request, "errors/user-does-not-exist.html")

    # Getting profile from current user
    profile = models.Profile.objects.get(user=user)

    # Grabbing all projects
    projects = list(profile.projects.all())

    # Grabbing all completed exercises
    completed_project_exercises = list(profile.completed_project_exercises.all())
    completed_quiz_exercises = list(profile.completed_quiz_exercises.all())

    return render(request, "app/profile/profile.html", context={
        "profile": profile,
        "projects": projects,
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
        locationName = request.POST.get("location")
        education = request.POST.get("education")
        skills = request.POST.get("skills").split(",")

        # Social Links
        facebook_profile = request.POST.get("facebook-profile")
        instagram_profile = request.POST.get("instagram-profile")
        linkedin_profile = request.POST.get("linkedin-profile")
        twitter_profile = request.POST.get("twitter-profile")
        github_profile = request.POST.get("github-profile")
        youtube_profile = request.POST.get("youtube-profile")
        medium_profile = request.POST.get("medium-profile")
        personal_website = request.POST.get("personal-website")

        # Check if username/email is used
        if (User.objects.filter(email=email).exists() and email != request.user.email) or (User.objects.filter(username=username).exists() and username != request.user.username):
            return render(request, "app/profile/edit-profile.html", context={
                "message": "Username and/or email is already taken. Please double check.",
                "status": "bad",
                "profile": profile
            })

        # Creating location object if exists
        location = None
        if locationName:
            response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={locationName}&key={settings.GOOGLE_API_KEY}")

            location = models.Location(name=locationName)
            if response.json()["results"]:
                location.lat = response.json()["results"][0]["geometry"]["location"]["lat"]
                location.lng = response.json()["results"][0]["geometry"]["location"]["lng"]

            location.save()

        # Updating user
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        # Updating profile
        profile = models.Profile.objects.get(user=request.user)
        profile.biography = biography
        profile.location = location
        profile.education = education
        profile.skills = skills
        profile.facebook_profile = facebook_profile
        profile.instagram_profile = instagram_profile
        profile.linkedin_profile = linkedin_profile
        profile.twitter_profile = twitter_profile
        profile.github_profile = github_profile
        profile.youtube_profile = youtube_profile
        profile.medium_profile = medium_profile
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

    skills = None
    if profile.skills:
        skills = ",".join(profile.skills)

    return render(request, "app/profile/edit-profile.html", context={
        "profile": profile,
        "skills": skills,
        "google_api_key": settings.GOOGLE_API_KEY
    })


@login_required(login_url="/login/")
def submit_project(request, username):
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
            "content": "We're sorry, but you don't have permission to submit a project for this user. Only the logged in user of this account has permission to submit a project for themselves."
        })

    if request.method == "POST":
        # Grabbing all pieces of form POST data
        # Grabbing default Django User data
        name = request.POST.get("name")
        description = request.POST.get("description")
        technologies_used = request.POST.get("technologies-used").split(",")
        github_link = request.POST.get("github-link")
        website = request.POST.get("website")
        video_link = request.POST.get("video-link")

        project = models.Project(
            name=name,
            description=description,
            technologies_used=technologies_used,
            github_link=github_link,
            website=website,
            video_link=video_link,
            creator=request.user.profile,
        )
        project.save()

        request.user.profile.projects.add(project)

        return HttpResponseRedirect("/@" + user.username)

    return render(request, "app/profile/submit-project.html")


@login_required(login_url="/login/")
def edit_project(request, username):
    # Getting current user
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        return render(request, "errors/does-not-exist", context={
            "title": "User doesn't exist!",
            "content": "We're sorry, but we couldn't find the user you were looking for! That user has either been removed, or never existed in the first place. Please go back to the previous page if possible."
        })

    # Getting profile from id
    project_id = request.GET.get("id")
    project = models.Project.objects.get(id=project_id)

    # Checking to see if current user is the one editing profile
    if user != request.user:
        return render(request, "errors/does-not-exist.html", context={
            "title": "Permission Error",
            "content": "We're sorry, but you don't have permission to edit this project. Only the logged in user of this account has permission to modify any of the content of their profile."
        })

    if request.method == "POST":
        # Grabbing all pieces of form POST data
        # Grabbing default Django User data
        name = request.POST.get("name")
        description = request.POST.get("description")
        technologies_used = request.POST.get("technologies-used").split(",")
        github_link = request.POST.get("github-link")
        website = request.POST.get("website")
        video_link = request.POST.get("video-link")

        # Updating profile
        project.name = name
        project.description = description
        project.technologies_used = technologies_used
        project.github_link = github_link
        project.website = website
        project.video_link = video_link

        project.save()

        return HttpResponseRedirect("/@" + user.username)

    technologies_used = None
    if project.technologies_used:
        technologies_used = ",".join(project.technologies_used)

    return render(request, "app/profile/edit-project.html", context={ "project": project, "technologies_used": technologies_used })
