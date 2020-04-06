from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required(login_url="http://www.w3hacks.com/login")
def index(request):
    return render(request, "hackathon/index.html")


# @login_required(login_url="http://www.w3hacks.com/login")
def competitors(request):
    return render(request, "hackathon/competitors.html")


# @login_required(login_url="http://www.w3hacks.com/login")
def schedule(request):
    return render(request, "hackathon/schedule.html")


# @login_required(login_url="http://www.w3hacks.com/login")
def submissions(request):
    return render(request, "hackathon/submissions.html")


# @login_required(login_url="http://www.w3hacks.com/login")
def submit(request):
    return render(request, "hackathon/submit.html")
