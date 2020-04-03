from django.shortcuts import render
from django.http import HttpResponseRedirect


def index(request):
    return HttpResponseRedirect("/hackathons/")

def hackathons(request):
    return render(request, "staff/hackathons.html")


def edit_hackathon(request):
    return render(request, "staff/edit-hackathon.html")


def create_hackathon(request):
    return render(request, "staff/create-hackathon.html")
