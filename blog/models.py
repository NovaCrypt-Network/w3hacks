from django.db import models
from datetime import date


class BlogPost(models.Model):
    url_extension = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    preview = models.TextField()
    body = models.TextField()
    date_posted = models.DateField(default=date.today())

    def __str__(self):
        return self.title
