from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from src.config.celery import app
from src.core.models import Point, WeatherCheckResult


@app.task()
def check_weather_for_all_locations():
    locations = Point.objects.filter(flight_time__gt=now())

    for location in locations:
        if now() >= location.flight_time:
            continue
        return check_weather_for_location.apply_async(args=[location.id])


@app.task()
def check_weather_for_location(location_id):
    location = get_object_or_404(Point, id=location_id)

    result = location.predict_weather()
    if result is None:
        return

    flight_weather, non_flight_reason = result

    WeatherCheckResult.objects.create(
        point=location,
        flight_weather=flight_weather,
        non_flight_reason=non_flight_reason,
    )

    return flight_weather
