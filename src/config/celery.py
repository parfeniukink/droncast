from os import environ

from celery import Celery
from celery.schedules import crontab

environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")
app = Celery("src.config")

app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check-weather-every-10-minutes": {
        "task": "src.core.tasks.check_weather_for_all_locations",
        "schedule": crontab(minute="*/10"),
    },
}
