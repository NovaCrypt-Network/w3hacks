from django.conf.urls import url
from . import views

urlpatterns = [
    url("^(?P<hackathon_id>[^/]+)/$", views.index, name="index"),
    url("^(?P<hackathon_id>[^/]+)/competitors/$", views.competitors, name="competitors"),
    url("^(?P<hackathon_id>[^/]+)/schedule/$", views.schedule, name="schedule"),
    url("^(?P<hackathon_id>[^/]+)/submissions/$", views.submissions, name="submissions"),
    url("^(?P<hackathon_id>[^/]+)/submit/$", views.submit, name="submit"),
]
