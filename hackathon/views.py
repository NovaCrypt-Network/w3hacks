from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import Hackathon


# @login_required(login_url="http://www.w3hacks.com/login")
def index(request, hackathon_id):
    hackathon = Hackathon.objects.get(id=hackathon_id)
    return render(request, "hackathon/index.html")


# @login_required(login_url="http://www.w3hacks.com/login")
def competitors(request, hackathon_id):
    return render(request, "hackathon/competitors.html")


# @login_required(login_url="http://www.w3hacks.com/login")
def schedule(request, hackathon_id):
    return render(request, "hackathon/schedule.html")


# @login_required(login_url="http://www.w3hacks.com/login")
def submissions(request, hackathon_id):
    return render(request, "hackathon/submissions.html")


# @login_required(login_url="http://www.w3hacks.com/login")
def submit(request, hackathon_id):
    return render(request, "hackathon/submit.html")
