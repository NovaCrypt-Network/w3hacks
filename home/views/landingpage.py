from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from datetime import datetime, date
from home import models


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/dashboard/")

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email_body = f"From: {name}\nEmail: {email}\n\n{message}"
        EmailMessage("w3Hacks Contact Us", email_body, to=["calix.huang1@gmail.com"]).send()

        return render(request, "home/index.html", context={
            "message": "Message sent!"
        })

    return render(request, "landingpage/index.html")


def contact(request):
    return render(request, "landingpage/contact.html")


def team(request):
    return render(request, "landingpage/team.html")


def join(request):
    return render(request, "landingpage/join.html")


def events(request):
    events = models.Event.objects.all().order_by('-datetime')
    return render(request, "landingpage/events.html", context={
        "events": events
    })


def news(request):
    updates = models.NewsUpdate.objects.all().order_by('-date_posted')
    return render(request, "landingpage/news.html", context={
        "updates": updates
    })


def blog(request):
    blogs = models.BlogPost.objects.all().order_by('-date_posted')
    return render(request, "landingpage/blog.html", context={
        "blogs": blogs,
    })

def blog_post(request, blog_url):
    if models.BlogPost.objects.filter(url_extension=blog_url).exists():
        blog = models.BlogPost.objects.get(url_extension=blog_url)
        return render(request, "landingpage/blog-post.html", context={
            "blog": blog
        })

    else:
        return render(request, "errors/blog-does-not-exist.html")
