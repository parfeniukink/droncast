from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WeatherLocation(models.Model):

    class Meta:
        db_table = "weather_location"

    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    flight_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
