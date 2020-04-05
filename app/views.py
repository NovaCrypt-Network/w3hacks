from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return render(request, "app/index.html")


def achievements(request):
    return render(request, "app/achievements.html")


def leaderboards(request):
    return render(request, "app/leaderboards.html")


# Activities views
def activites(request):
    return render(request, "app/activites.html")


def project_exercises(request):
    return render(request, "app/project-exercises.html")


def quiz_exercises(request):
    return render(request, "app/quiz-exercises.html")


def mini_exercises(request):
    return render(request, "app/mini-exercises.html")


# Hackathon views
def hackathon(request):
    return render(request, "app/hackathon.html")


def about_the_hackathon(request):
    return render(request, "app/about-the-hackathon.html")


def past_hackathons(request):
    return render(request, "app/past-hackathons.html")


def future_hackathons(request):
    return render(request, "app/future-hackathons.html")


# Profile views
def profile(request):
    return render(request, "app/profile.html")


def edit_profile(request):
    return render(request, "app/edit-profile.html")


def user_logout(request):
    return HttpResponse("Logout")
