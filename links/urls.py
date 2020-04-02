from django.conf.urls import url
from . import views

urlpatterns = [
    url("^(?P<url_extension>[^/]+)/$", views.link, name="link"),
]
