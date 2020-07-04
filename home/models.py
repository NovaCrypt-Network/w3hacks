from django.db import models
from datetime import datetime, date

class NewsUpdate(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    date_posted = models.DateField(default=date.today())

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    url_extension = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    preview = models.TextField()
    body = models.TextField()
    date_posted = models.DateField(default=date.today())

    def __str__(self):
        return self.title


class Event(models.Model):
    url_extension = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    preview = models.TextField()
    body = models.TextField()
    datetime = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title
