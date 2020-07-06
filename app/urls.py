from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
from . import views as views
from hackathon import views as hackathonViews

urlpatterns = [
    url('admin/', admin.site.urls),
    url("^$", views.index, name="index"),
]

urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
