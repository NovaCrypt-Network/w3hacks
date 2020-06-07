from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views as views
from hackathon import views as hackathonViews

urlpatterns = [
    url('admin/', admin.site.urls),
    url("^$", views.index, name="index"),
    url("^login/$", views.user_login, name="login"),
    url("^register/$", views.register, name="register"),

    url("^leaderboards/$", views.leaderboards, name="leaderboards"),

    # Activities URL routes
    url("^exercises/$", views.exercises, name="exercises"),
    url("^exercises/project-exercises/$", views.project_exercises, name="project_exercises"),
    url("^exercises/project-exercises/exercise/$", views.project_exercise, name="project_exercise"),

    url("^exercises/quiz-exercises/$", views.quiz_exercises, name="quiz_exercises"),
    url("^exercises/quiz-exercises/exercise/$", views.quiz_exercise, name="quiz_exercise"),
    url("^exercises/quiz-exercises/exercise/take-quiz/$", views.take_quiz, name="take_quiz"),
    url("^exercises/quiz-exercises/exercise/quiz-results/$", views.quiz_results, name="quiz_results"),

    url("^exercises/mini-exercises/$", views.mini_exercises, name="mini_exercises"),
    url("^exercises/mini-exercises/fix-the-code-exercises/$", views.fix_the_code_exercises),
    url("^exercises/mini-exercises/fix-the-code-exercises/exercise/$", views.fix_the_code_exercise, name="fix_the_code_exercise"),
    url("^exercises/mini-exercises/brainteaser-exercises/$", views.brainteaser_exercises, name="brainteaser_exercises"),
    url("^exercises/mini-exercises/brainteaser-exercises/exercise/$", views.brainteaser_exercise, name="brainteaser_exercise"),
    url("^exercises/mini-exercises/visualization-exercises/$", views.visualization_exercises, name="visualization_exercises"),
    url("^exercises/mini-exercises/visualization-exercises/exercise/$", views.visualization_exercise, name="visualization_exercise"),
    url("^exercises/mini-exercises/refactor-exercises/$", views.refactor_exercises, name="refactor_exercises"),
    url("^exercises/mini-exercises/refactor-exercises/exercise/$", views.refactor_exercise, name="refactor_exercise"),
    url("^exercises/mini-exercises/teaching-exercises/$", views.teaching_exercises, name="teaching_exercises"),
    url("^exercises/mini-exercises/teaching-exercises/exercise/$", views.teaching_exercise, name="teaching_exercise"),
    url("^exercises/mini-exercises/github-exercises/$", views.github_exercises, name="github_exercises"),
    url("^exercises/mini-exercises/github-exercises/exercise/$", views.github_exercise, name="github_exercise"),
    url("^exercises/mini-exercises/research-exercises/$", views.research_exercises, name="research_exercises"),
    url("^exercises/mini-exercises/research-exercises/exercise/$", views.research_exercise, name="research_exercise"),

    # Hackathon views
    url("^about-the-hackathon/$", views.about_the_hackathon, name="about_the_hackathon"),
    url("^past-hackathons/$", views.past_hackathons, name="past_hackathons"),
    url("^future-hackathons/$", views.future_hackathons, name="future_hackathons"),

    # Profile views
    url("^profile/(?P<user_id>[^/]+)/$", views.profile, name="profile"),
    url("^edit-profile/(?P<user_id>[^/]+)/$", views.edit_profile, name="edit_profile"),
    url("^logout/$", views.user_logout, name="logout"),

    # API views
    url("create-completed-quiz-exercise/$", views.create_completed_quiz_exercise, name="create_completed_quiz_exercise"),

    # # Hackathon views
    # url("^(?P<hackathon_id>[^/]+)/$", hackathonViews.index, name="index"),
    # url("^(?P<hackathon_id>[^/]+)/competitors/$", hackathonViews.competitors, name="competitors"),
    # url("^(?P<hackathon_id>[^/]+)/schedule/$", hackathonViews.schedule, name="schedule"),
    # url("^(?P<hackathon_id>[^/]+)/submissions/$", hackathonViews.submissions, name="submissions"),
    # url("^(?P<hackathon_id>[^/]+)/submit/$", hackathonViews.submit, name="submit"),
    # url("^(?P<hackathon_id>[^/]+)/awards/$", hackathonViews.awards, name="awards"),
    # url("^(?P<hackathon_id>[^/]+)/profile/(?P<user_id>[^/]+)/$", hackathonViews.profile, name="profile"),
    # url("^(?P<hackathon_id>[^/]+)/edit-profile/(?P<user_id>[^/]+)/$", hackathonViews.edit_profile, name="edit_profile"),
]

urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
