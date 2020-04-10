from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from main import models

def index(request):
    return HttpResponse("Welcome to the w3Hacks API!")


@csrf_exempt
def add_competitor_to_hackathon(request):
    hackathon_id = request.GET.get("hackathon_id")
    user_id = request.GET.get("user_id")

    hackathon = models.Hackathon.objects.get(id=hackathon_id)
    profile = models.Profile.objects.get(user=User.objects.get(id=user_id))

    if not profile in list(hackathon.competitors.all()):
        hackathon.competitors.add(profile)
        hackathon.save()

    return JsonResponse({
        "status": 200
    })
