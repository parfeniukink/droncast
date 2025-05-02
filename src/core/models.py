from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from django_admin_geomap import GeoItem

from src.core.coordinates_utils import generate_coordinates_within_radius
from src.core.weather_service import weather_forecast_service

User = get_user_model()


class Point(models.Model, GeoItem):

    class Meta:
        db_table = "points"

    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    flight_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def geomap_longitude(self):
        return str(self.longitude)

    @property
    def geomap_latitude(self):
        return str(self.latitude)

    def predict_weather(self) -> tuple[bool, str | None] | None:
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
                return False, "precipitation"

        return True, None


class WeatherCheckResult(models.Model):
    class Meta:
        db_table = "weather_check_results"

    point = models.ForeignKey("Point", on_delete=models.CASCADE)
    flight_weather = models.BooleanField()
    non_flight_reason = models.CharField(max_length=255, null=True, blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        checked_time = self.checked_at.strftime("%Y-%m-%d %H:%M")
        flight_time = self.point.flight_time.strftime("%Y-%m-%d %H:%M")
        return (
            f"Weather checked at {checked_time} for point {self.point.id}"
            f"({self.point.latitude}, {self.point.longitude}) "
            f"with flight time {flight_time}"
        )
