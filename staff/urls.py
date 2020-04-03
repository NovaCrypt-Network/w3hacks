from django.conf.urls import url
from . import views

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^hackathons/$", views.hackathons, name="hackathons"),
    url("^edit-hackathon/$", views.edit_hackathon, name="edit_hackathon"),
    url("^create-hackathon/$", views.create_hackathon, name="create_hackathon"),
]
