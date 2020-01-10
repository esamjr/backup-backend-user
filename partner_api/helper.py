from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def get_scheme():
    scheme = 'http' if settings.DEBUG else 'https'
    return scheme + '://'


def get_full_current_site(request=None):
    return get_scheme() + get_current_site(request).domain
