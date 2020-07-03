from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from main.models import ResourceLink

def index(request):
    links = ResourceLink.objects.all()
    return render(request, "links/index.html", context={
        "links": links
    })

def link(request, url_extension):
    # Link exists
    if ResourceLink.objects.filter(url_extension=url_extension).exists():
        resource_link = ResourceLink.objects.get(url_extension=url_extension)
        return HttpResponseRedirect(resource_link.link)

    # Link doesn't exist
    else:
        return HttpResponse("That link doesn't exist.")
