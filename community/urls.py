from django.conf.urls import url
from . import views

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^leaderboards/$", views.leaderboards, name="leaderboards"),
    url("^past-hackathons/$", views.past_hackathons, name="past_hackathons"),
    url("^hackathon-schedule/$", views.hackathon_schedule, name="hackathon_schedule"),
    url("^login/$", views.user_login, name="user_login"),
    url("^logout/$", views.user_logout, name="user_logout"),
    url("^register/$", views.register, name="register"),
    url("^profile/$", views.profile, name="profile"),
    url("^edit-profile/$", views.edit_profile, name="edit_profile"),
    url("^hackathon/$", views.hackathon, name="hackathon"),
    url("^project/$", views.project, name="project"),
]
