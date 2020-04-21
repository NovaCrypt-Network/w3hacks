from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views
from hackathon import views as hackathonViews
from app import views as appViews

urlpatterns = [
    url('admin/', admin.site.urls),
    url("^$", views.index, name="index"),
    url("^about/$", views.about, name="about"),
    url("^contact/$", views.contact, name="contact"),
    url("^login/$", views.user_login, name="login"),
    url("^register/$", views.register, name="register"),

    # # Hackathon views
    # url("^(?P<hackathon_id>[^/]+)/$", hackathonViews.index, name="index"),
    # url("^(?P<hackathon_id>[^/]+)/competitors/$", hackathonViews.competitors, name="competitors"),
    # url("^(?P<hackathon_id>[^/]+)/schedule/$", hackathonViews.schedule, name="schedule"),
    # url("^(?P<hackathon_id>[^/]+)/submissions/$", hackathonViews.submissions, name="submissions"),
    # url("^(?P<hackathon_id>[^/]+)/submit/$", hackathonViews.submit, name="submit"),
    # url("^(?P<hackathon_id>[^/]+)/awards/$", hackathonViews.awards, name="awards"),

    # # App views
    # url("^$", appViews.index, name="index"),
    # url("^achievements/$", appViews.achievements, name="achievements"),
    # url("^leaderboards/$", appViews.leaderboards, name="leaderboards"),
    #
    # # Activities URL routes
    # url("^exercises/$", appViews.exercises, name="exercises"),
    # url("^exercises/project-exercises/$", appViews.project_exercises, name="project_exercises"),
    # url("^exercises/project-exercises/exercise/$", appViews.project_exercise, name="project_exercise"),
    #
    # url("^exercises/quiz-exercises/$", appViews.quiz_exercises, name="quiz_exercises"),
    # url("^exercises/quiz-exercises/exercise/$", appViews.quiz_exercise, name="quiz_exercise"),
    # url("^exercises/quiz-exercises/exercise/take-quiz/$", appViews.take_quiz, name="take_quiz"),
    # url("^exercises/quiz-exercises/exercise/quiz-results/$", appViews.quiz_results, name="quiz_results"),
    #
    # url("^exercises/mini-exercises/$", appViews.mini_exercises, name="mini_exercises"),
    # url("^exercises/mini-exercises/fix-the-code-exercises/$", appViews.fix_the_code_exercises),
    # url("^exercises/mini-exercises/fix-the-code-exercises/exercise/$", appViews.fix_the_code_exercise, name="fix_the_code_exercise"),
    # url("^exercises/mini-exercises/brainteaser-exercises/$", appViews.brainteaser_exercises, name="brainteaser_exercises"),
    # url("^exercises/mini-exercises/brainteaser-exercises/exercise/$", appViews.brainteaser_exercise, name="brainteaser_exercise"),
    # url("^exercises/mini-exercises/visualization-exercises/$", appViews.visualization_exercises, name="visualization_exercises"),
    # url("^exercises/mini-exercises/visualization-exercises/exercise/$", appViews.visualization_exercise, name="visualization_exercise"),
    # url("^exercises/mini-exercises/refactor-exercises/$", appViews.refactor_exercises, name="refactor_exercises"),
    # url("^exercises/mini-exercises/refactor-exercises/exercise/$", appViews.refactor_exercise, name="refactor_exercise"),
    # url("^exercises/mini-exercises/teaching-exercises/$", appViews.teaching_exercises, name="teaching_exercises"),
    # url("^exercises/mini-exercises/teaching-exercises/exercise/$", appViews.teaching_exercise, name="teaching_exercise"),
    # url("^exercises/mini-exercises/github-exercises/$", appViews.github_exercises, name="github_exercises"),
    # url("^exercises/mini-exercises/github-exercises/exercise/$", appViews.github_exercise, name="github_exercise"),
    # url("^exercises/mini-exercises/research-exercises/$", appViews.research_exercises, name="research_exercises"),
    # url("^exercises/mini-exercises/research-exercises/exercise/$", appViews.research_exercise, name="research_exercise"),
    #
    # # Hackathon views
    # url("^about-the-hackathon/$", appViews.about_the_hackathon, name="about_the_hackathon"),
    # url("^past-hackathons/$", appViews.past_hackathons, name="past_hackathons"),
    # url("^future-hackathons/$", appViews.future_hackathons, name="future_hackathons"),
    #
    # # Profile views
    # url("^profile/(?P<user_id>[^/]+)/$", appViews.profile, name="profile"),
    # url("^edit-profile/(?P<user_id>[^/]+)/$", appViews.edit_profile, name="edit_profile"),
    # url("^logout/$", appViews.user_logout, name="logout"),
    #
    # # API views
    # url("create-completed-quiz-exercise/$", appViews.create_completed_quiz_exercise, name="create_completed_quiz_exercise"),
]

urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
