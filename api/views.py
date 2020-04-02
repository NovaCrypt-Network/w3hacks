from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def index(request):
    return HttpResponse("Welcome to the w3Hacks API!")
