from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    url("^$", views.index_redirect, name="index_redirect"),
    url("^(?P<hackathon_id>[^/]+)/$", views.index, name="index"),
    url("^(?P<hackathon_id>[^/]+)/competitors/$", views.competitors, name="competitors"),
    url("^(?P<hackathon_id>[^/]+)/schedule/$", views.schedule, name="schedule"),
    url("^(?P<hackathon_id>[^/]+)/submissions/$", views.submissions, name="submissions"),
    url("^(?P<hackathon_id>[^/]+)/submit/$", views.submit, name="submit"),
    url("^(?P<hackathon_id>[^/]+)/awards/$", views.awards, name="awards"),
    url("^(?P<hackathon_id>[^/]+)/profile/(?P<user_id>[^/]+)/$", views.profile, name="profile"),
    url("^(?P<hackathon_id>[^/]+)/edit-profile/(?P<user_id>[^/]+)/$", views.edit_profile, name="edit_profile"),
]

urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
