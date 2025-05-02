from os import environ

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")
app = Celery("src.config")

app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks()

app.conf.beat_schedule = {
    f"check-weather-every-{settings.DC_WEATHER_CHECK_INTERVAL}-minutes": {
        "task": "src.core.tasks.check_weather_for_all_locations",
        "schedule": crontab(minute=f"*/{settings.DC_WEATHER_CHECK_INTERVAL}"),
    },
}
