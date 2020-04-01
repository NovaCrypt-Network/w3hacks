from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', 'landingpage.urls', name='www'),
    host(r'community', 'community.urls', name='community'),
)
