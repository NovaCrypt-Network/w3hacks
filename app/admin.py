from django.contrib import admin
from django.apps import apps
from app import models as app_models
from home import models as home_models
from blog import models as blog_models

models_list = [
    # App Models
    app_models.Profile,
    app_models.Project,
    app_models.ProjectImplementation,
    app_models.ProjectExercise,
    app_models.CompletedProjectExercise,
    app_models.QuizExercise,
    app_models.QuizQuestion,
    app_models.CompletedQuizExercise,
    app_models.ResourceLink,

    # Home models
    home_models.NewsUpdate,
    home_models.Event,

    # Blog models
    blog_models.BlogPost,
]

for model in models_list:
    admin.site.register(model)
