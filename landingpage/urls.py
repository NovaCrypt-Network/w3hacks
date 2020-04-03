from django.contrib import admin
from django.conf.urls import url
from . import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url("^$", views.index, name="index"),
    url("^about/$", views.about, name="about"),
    url("^contact/$", views.contact, name="contact"),
]
