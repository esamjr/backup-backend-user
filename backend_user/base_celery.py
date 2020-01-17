from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    'get_data_timesheet_absense': {
        'task': 'get_data_timesheet_absense',
        'schedule': crontab(minute=5, hour=1),
    },
    'get_data_leave_absense': {
        'task': 'get_data_leave_absense',
        'schedule': crontab(minute=5, hour=1),
    },
}
