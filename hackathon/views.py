from django.shortcuts import render

def index(request):
    return render(request, "hackathon/index.html")


def competitors(request):
    return render(request, "hackathon/competitors.html")


def schedule(request):
    return render(request, "hackathon/schedule.html")


def submissions(request):
    return render(request, "hackathon/submissions.html")


def submit(request):
    return render(request, "hackathon/submit.html")
