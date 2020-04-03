from django.shortcuts import render

def index(request):
    return render(request, "community/index.html")


def leaderboards(request):
    return render(request, "community/leaderboards.html")


def past_hackathons(request):
    return render(request, "community/past-hackathons.html")


def hackathon_schedule(request):
    return render(request, "community/hackathon-schedule.html")


def user_login(request):
    return render(request, "community/login.html")


def user_logout(request):
    return render(request, "community/logout.html")


def register(request):
    return render(request, "community/register.html")


def profile(request):
    return render(request, "community/profile.html")


def edit_profile(request):
    return render(request, "community/edit-profile.html")


def hackathon(request):
    return render(request, "community/hackathon.html")


def project(request):
    return render(request, "community/project.html")
