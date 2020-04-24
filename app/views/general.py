from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from main import models
from datetime import datetime
import json


@login_required(login_url="http://www.w3hacks.com/login")
def index(request):
    return render(request, "app/index.html")


@login_required(login_url="http://www.w3hacks.com/login")
def achievements(request):
    achievements = models.Achievement.objects.all()

    my_achievements = list(models.Profile.objects.get(user=request.user).achievements.all())

    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Achievements", "link": "/achievements/"}
    ]

    return render(request, "app/achievements.html", context={
        "achievements": achievements,
        "my_achievements": my_achievements,
        "breadcrumbs": breadcrumbs
    })


@login_required(login_url="http://www.w3hacks.com/login")
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

    return render(request, "app/leaderboards.html", context={
        "overall_rankings": overall_rankings,
        "project_rankings": project_rankings,
        "quiz_rankings": quiz_rankings,
        "exercise_rankings": exercise_rankings,
        "breadcrumbs": breadcrumbs
    })


# Activities views
@login_required(login_url="http://www.w3hacks.com/login")
def exercises(request):
    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "Exercises", "link": "/exercises/"}
    ]

    return render(request, "app/exercises/exercises.html", context={
        "breadcrumbs": breadcrumbs
    })


# Hackathon views
@login_required(login_url="http://www.w3hacks.com/login")
def about_the_hackathon(request):
    # Creating breadcrumbs
    breadcrumbs = [
        { "text": "Home", "link": "/" },
        { "text": "About The Hackathon", "link": "/about-the-hackathon/"}
    ]

    return render(request, "app/hackathon/about-the-hackathon.html", context={
        "breadcrumbs": breadcrumbs
    })


@login_required(login_url="http://www.w3hacks.com/login")
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

    return render(request, "app/hackathon/past-hackathons.html", context={
        "past_hackathons": past_hackathons,
        "breadcrumbs": breadcrumbs
    })


@login_required(login_url="http://www.w3hacks.com/login")
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

    return render(request, "app/hackathon/future-hackathons.html", context={
        "future_hackathons": future_hackathons,
        "breadcrumbs": breadcrumbs
    })


# Profile views
@login_required(login_url="http://www.w3hacks.com/login")
def profile(request, user_id):
    # Getting current user
    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
    else:
        return render(request, "errors/user-does-not-exist.html")

    # Getting profile from current user
    profile = models.Profile.objects.get(user=user)

    # Grabbing all past hackathons for current user
    past_hackathons = list(profile.past_hackathons.all())

    # Grabbing all completed achievements
    achievements = list(profile.achievements.all())

    # Grabbing all completed exercises
    completed_project_exercises = list(profile.completed_project_exercises.all())
    completed_quiz_exercises = list(profile.completed_quiz_exercises.all())
    completed_fix_the_code_exercises = list(profile.completed_fix_the_code_exercises.all())
    completed_brainteaser_exercises = list(profile.completed_brainteaser_exercises.all())
    completed_visualization_exercises = list(profile.completed_visualization_exercises.all())
    completed_refactor_exercises = list(profile.completed_refactor_exercises.all())
    completed_teaching_exercises = list(profile.completed_teaching_exercises.all())
    completed_github_exercises = list(profile.completed_github_exercises.all())
    completed_research_exercises = list(profile.completed_research_exercises.all())

    return render(request, "app/profile.html", context={
        "profile": profile,
        "skills": ",".join(profile.skills),
        "past_hackathons": past_hackathons,
        "achievements": achievements,
        "completed_project_exercises": completed_project_exercises,
        "completed_quiz_exercises": completed_quiz_exercises,
        "completed_fix_the_code_exercises": completed_fix_the_code_exercises,
        "completed_brainteaser_exercises": completed_brainteaser_exercises,
        "completed_visualization_exercises": completed_visualization_exercises,
        "completed_refactor_exercises": completed_refactor_exercises,
        "completed_teaching_exercises": completed_teaching_exercises,
        "completed_github_exercises": completed_github_exercises,
        "completed_research_exercises": completed_research_exercises,
    })


@login_required(login_url="http://www.w3hacks.com/login")
def edit_profile(request, user_id):
    # Getting current user
    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
    else:
        return render(request, "errors/user-does-not-exist.html")

    # Getting profile from current user
    profile = models.Profile.objects.get(user=user)

    # Checking to see if current user is the one editing profile
    if user == request.user:
        pass
    else:
        return HttpResponse("You do not have permission to modify this profile.")

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

        # Checking if they provided picture
        if 'profile-picture' in request.FILES:
            profile.profile_picture = request.FILES['profile-picture']

        user.save()
        profile.save()

        return HttpResponseRedirect("/profile/" + str(user.id))


    return render(request, "app/edit-profile.html", context={
        "profile": profile,
        "skills": ",".join(profile.skills)
    })


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("http://w3hacks.com")
