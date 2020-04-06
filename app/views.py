from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required(login_url="http://www.w3hacks.com/login")
def index(request):
    return render(request, "app/index.html")


@login_required(login_url="http://www.w3hacks.com/login")
def achievements(request):
    return render(request, "app/achievements.html")


@login_required(login_url="http://www.w3hacks.com/login")
def leaderboards(request):
    return render(request, "app/leaderboards.html")


# Activities views
@login_required(login_url="http://www.w3hacks.com/login")
def activites(request):
    return render(request, "app/activites.html")


@login_required(login_url="http://www.w3hacks.com/login")
def project_exercises(request):
    return render(request, "app/project-exercises.html")


@login_required(login_url="http://www.w3hacks.com/login")
def quiz_exercises(request):
    return render(request, "app/quiz-exercises.html")


@login_required(login_url="http://www.w3hacks.com/login")
def mini_exercises(request):
    return render(request, "app/mini-exercises.html")


# Hackathon views
@login_required(login_url="http://www.w3hacks.com/login")
def hackathon(request):
    return render(request, "app/hackathon.html")


@login_required(login_url="http://www.w3hacks.com/login")
def about_the_hackathon(request):
    return render(request, "app/about-the-hackathon.html")


@login_required(login_url="http://www.w3hacks.com/login")
def past_hackathons(request):
    return render(request, "app/past-hackathons.html")


@login_required(login_url="http://www.w3hacks.com/login")
def future_hackathons(request):
    return render(request, "app/future-hackathons.html")


# Profile views
@login_required(login_url="http://www.w3hacks.com/login")
def profile(request):
    return render(request, "app/profile.html")


@login_required(login_url="http://www.w3hacks.com/login")
def edit_profile(request):
    return render(request, "app/edit-profile.html")


def user_logout(request):
    logout(request)
    return HttpResponse("Logout")
