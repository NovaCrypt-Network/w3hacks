from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
from . import views as views
from hackathon import views as hackathonViews

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^contact/$", views.contact, name="contact"),
    url("^team/$", views.team, name="team"),
    url("^join/$", views.join, name="join"),
    url("^faqs/$", views.faqs, name="faqs"),
    url("^events/$", views.events, name="events"),
    url("^events/(?P<event_url>[^/]+)$", views.event, name="event"),

    # Legal
    url("^terms-of-service/$", views.terms_of_service, name="terms_of_service"),
    url("^privacy-policy/$", views.privacy_policy, name="privacy_policy"),
    url("^code-of-conduct/$", views.code_of_conduct, name="code_of_conduct"),
]

urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
