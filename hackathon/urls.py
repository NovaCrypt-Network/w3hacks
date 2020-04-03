from django.conf.urls import url
from . import views

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^competitors/$", views.competitors, name="competitors"),
    url("^schedule/$", views.schedule, name="schedule"),
    url("^submissions/$", views.submissions, name="submissions"),
    url("^submit/$", views.submit, name="submit"),
]
