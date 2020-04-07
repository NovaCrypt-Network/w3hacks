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
]

urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
