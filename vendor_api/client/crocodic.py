import json
import requests
import logging

from rest_framework import status
from django.conf import settings
from celery import task

logger = logging.getLogger(settings.GET_LOGGER_NAME)


class CrocodicClient(object):
    """CROCODIC Client"""
    def __init__(self, url):
        self.url = url

    @task(name='get_data_timesheet_absense')
    def get_data_timesheet_absense(request):
        try:
            params = {
                "date_start": '2020-01-01',
                "date_end": '2020-01-31',
                "id_companies": 49
            }

            response = requests.get(settings.CROCODIC_API_URL + 'time-sheet?', params=params)
            data = json.loads(response.content)

            if response.status_code == status.HTTP_200_OK:
                return data
            else:
                logger.error({
                    'errorType': 404,
                    'message': 'Unknown resources from Crocodic'
                })
                return False
        except Exception as ex:
            logger.error({
                'errorType': 500,
                'message': ex.args
            })
        return False


