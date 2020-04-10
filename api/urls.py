from django.conf.urls import url
from . import views

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^add-competitor-to-hackathon/$", views.add_competitor_to_hackathon, name="add_competitor_to_hackathon"),
]
