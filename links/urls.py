from django.conf.urls import url
from . import views

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^(?P<url_extension>[^/]+)/$", views.link, name="link"),
]
