import logging

from django.conf import settings
from django.template.loader import render_to_string
from .helper import get_scheme, get_full_current_site
from django.contrib.sites.shortcuts import get_current_site

logger = logging.getLogger(settings.GET_LOGGER_NAME)


def render_to_string_with_context(template_path, **kwargs):
    domain = kwargs.get('domain')
    scheme = kwargs.get('scheme')
    if not domain:
        domain = get_current_site(None).domain
    if not scheme:
        scheme = get_scheme()

    kwargs.update({
        'domain': domain,
        'scheme': scheme,
        'homepage_url': get_full_current_site(),
    })
    message = render_to_string(template_path, kwargs)
    return message



