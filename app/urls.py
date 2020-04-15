from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^achievements/$", views.achievements, name="achievements"),
    url("^leaderboards/$", views.leaderboards, name="leaderboards"),

    # Activities URL routes
    url("^exercises/$", views.exercises, name="exercises"),
    url("^exercises/project-exercises/$", views.project_exercises, name="project_exercises"),
    url("^exercises/project-exercises/exercise/$", views.project_exercise, name="project_exercise"),

    url("^exercises/quiz-exercises/$", views.quiz_exercises, name="quiz_exercises"),
    url("^exercises/quiz-exercises/exercise/$", views.quiz_exercise, name="quiz_exercise"),
    url("^exercises/quiz-exercises/exercise/quiz-results/$", views.quiz_results, name="quiz_results"),

    url("^exercises/mini-exercises/$", views.mini_exercises, name="mini_exercises"),
    url("^exercises/mini-exercises/exercise/$", views.mini_exercise, name="mini_exercise"),

    # Hackathon views
    url("^hackathon/$", views.hackathon, name="hackathon"),
    url("^about-the-hackathon/$", views.about_the_hackathon, name="about_the_hackathon"),
    url("^past-hackathons/$", views.past_hackathons, name="past_hackathons"),
    url("^future-hackathons/$", views.future_hackathons, name="future_hackathons"),

    # Profile views
    url("^profile/(?P<user_id>[^/]+)/$", views.profile, name="profile"),
    url("^edit-profile/(?P<user_id>[^/]+)/$", views.edit_profile, name="edit_profile"),
    url("^logout/$", views.user_logout, name="logout"),

    # API views
    url("create-completed-quiz-exercise/$", appViews.create_completed_quiz_exercise, name="create_completed_quiz_exercise"),
]

urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
