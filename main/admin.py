from django.contrib import admin
from django.apps import apps

# Grabbing all models
models = apps.get_models()

# Iterating through all models
for model in models:
    # Register the model
    try:
        admin.site.register(model)

    # Pass if model is already registered
    except admin.sites.AlreadyRegistered:
        pass
