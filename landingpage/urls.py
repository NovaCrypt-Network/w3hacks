from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url("^$", views.index, name="index"),
    url("^about/$", views.about, name="about"),
    url("^contact/$", views.contact, name="contact"),
    url("^login/$", views.user_login, name="login"),
    url("^register/$", views.register, name="register"),
]

urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
