from django.shortcuts import render
from django.http import HttpResponseRedirect

def index(request):
    return HttpResponseRedirect("https://www.calix.dev/")
