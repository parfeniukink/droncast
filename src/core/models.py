from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from src.core.coordinates_utils import generate_coordinates_within_radius
from src.core.weather_service import weather_forecast_service

User = get_user_model()


class Point(models.Model):

    class Meta:
        db_table = "weather_location"

    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    flight_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def predict_weather(self) -> bool | None:
        if now() >= self.flight_time:
            return

        today = now().date()
        delta = (self.flight_time.date() - today).days
        forecast_days = delta + 1

        coords_list = generate_coordinates_within_radius(
            self.latitude,
            self.longitude,
            self.radius,
        )

        for lat, lon in coords_list:
            if not weather_forecast_service.precipitation_check(
                lat=lat,
                lon=lon,
                forecast_days=forecast_days,
                flight_time=self.flight_time,
            ):
                return False

        return True
