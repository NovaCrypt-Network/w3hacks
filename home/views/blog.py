from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from datetime import datetime, date
from home import models

def blog(request):
    blogs = models.BlogPost.objects.all()
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
