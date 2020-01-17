import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def get_crocodic_client():
    from .crocodic import CrocodicClient
    return CrocodicClient(settings.CROCODIC_API_URL)
