from django.shortcuts import render
from blog import models


def index(request):
    blogs = models.BlogPost.objects.all().order_by('-date_posted')
    return render(request, "blog/index.html", context={
        "blogs": blogs,
    })

def post(request, blog_url):
    if models.BlogPost.objects.filter(url_extension=blog_url).exists():
        blog = models.BlogPost.objects.get(url_extension=blog_url)
        return render(request, "blog/post.html", context={
            "blog": blog
        })

    else:
        return render(request, "errors/does-not-exist.html", context={
            "title": "Blog post doesn't exist!",
            "content": "We're sorry, but we couldn't find the blog post you were looking for! It has either been removed, or you have navigated to the wrong page. Please go back to the previous page if possible."
        })
