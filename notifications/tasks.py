import time

from celery import shared_task

from .models import NotificationSettings
from .utils import schedule_executor_notification


@shared_task
def notifications_task(*args, **kwargs):
    settings = NotificationSettings.objects.filter(notification_type=0).first()
    if settings:
        while True:
            time.sleep(settings.delay_time * 60)
            schedule_executor_notification()
