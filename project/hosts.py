from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', 'landingpage.urls', name='www'),
    host(r'api', 'api.urls', name='api'),
    host(r'app', 'app.urls', name='app'),
    host(r'hackathon', 'hackathon.urls', name='hackathon'),
    host(r'links', 'links.urls', name='links'),
)
