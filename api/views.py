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
    user = User.objects.get(id=user_id)
    profile = models.Profile.objects.get(user=user)

    # Making sure that the user isn't a competitor already and the person making the request is logged in to the respective user's account
    if not profile in list(hackathon.competitors.all()) and user == request.user:
        hackathon.competitors.add(profile)
        hackathon.save()

        # Adding hackathon to past hackathons for user
        profile.past_hackathons.add(hackathon)
        profile.save()

    return JsonResponse({
        "status": 200
    })
