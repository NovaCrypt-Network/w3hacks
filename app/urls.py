from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^achievements/$", appViews.achievements, name="achievements"),
    url("^leaderboards/$", appViews.leaderboards, name="leaderboards"),

    # Activities URL routes
    url("^exercises/$", appViews.exercises, name="exercises"),
    url("^exercises/project-exercises/$", appViews.project_exercises, name="project_exercises"),
    url("^exercises/quiz-exercises/$", appViews.quiz_exercises, name="quiz_exercises"),
    url("^exercises/mini-exercises/$", appViews.mini_exercises, name="mini_exercises"),

    # Hackathon views
    url("^hackathon/$", appViews.hackathon, name="hackathon"),
    url("^about-the-hackathon/$", appViews.about_the_hackathon, name="about_the_hackathon"),
    url("^past-hackathons/$", appViews.past_hackathons, name="past_hackathons"),
    url("^future-hackathons/$", appViews.future_hackathons, name="future_hackathons"),

    # Profile views
    url("^profile/(?P<user_id>[^/]+)/$", appViews.profile, name="profile"),
    url("^edit-profile/(?P<user_id>[^/]+)/$", appViews.edit_profile, name="edit_profile"),
    url("^logout/$", appViews.user_logout, name="logout"),
]

urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
