from django.contrib import admin
from django.apps import apps
from app import models as app_models
from home import models as home_models

models_list = [
    # App Models
    app_models.Profile,
    app_models.Project,
    app_models.ProjectExercise,
    app_models.CompletedProjectExercise,
    app_models.QuizExercise,
    app_models.CompletedQuizExercise,
    app_models.ResourceLink,

    # Home models
    home_models.NewsUpdate,
    home_models.BlogPost,
    home_models.Event,
]

for model in models_list:
    admin.site.register(model)
