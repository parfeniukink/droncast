from datetime import datetime

import requests
from django.conf import settings
from django.utils.timezone import now

from src.config import DATE_TIME_FORMAT
from src.config.celery import app
from src.core.coordinates_utils import generate_coordinates_within_radius
from src.core.models import WeatherLocation


@app.task()
def check_weather_for_all_locations():
    locations = WeatherLocation.objects.filter(flight_time__gt=now())

    for location in locations:
        if now() >= location.flight_time:
            continue
        check_weather_for_location.apply_async(args=[location.id])


@app.task()
def check_weather_for_location(location_id):
    location = WeatherLocation.objects.get(id=location_id)

    if now() >= location.flight_time:
        return

    today = now().date()

    delta = (location.flight_time.date() - today).days
    forecast_days = delta + 1

    coords_list = generate_coordinates_within_radius(
        location.latitude,
        location.longitude,
        location.radius,
    )

    is_good_weather_overall = True

    for lat, lon in coords_list:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=precipitation&daily=precipitation_sum&forecast_days={forecast_days}&timezone=Europe/Kyiv"  # noqa

        response = requests.get(url)

        if response.status_code != 200:
            continue

        data = response.json()

        flight_time_str = location.flight_time.strftime(DATE_TIME_FORMAT)
        flight_time_obj = datetime.strptime(flight_time_str, DATE_TIME_FORMAT)

        matching_precipitation = next(
            (
                p
                for t, p in zip(
                    data["hourly"]["time"], data["hourly"]["precipitation"]
                )
                if datetime.strptime(t, DATE_TIME_FORMAT) == flight_time_obj
            ),
            None,
        )

        if matching_precipitation is not None:
            if matching_precipitation >= settings.DC_MAX_PRECIPITATION_MM:
                is_good_weather_overall = False
                print(
                    f"!!! Bad weather! Big amount of precipitations!!! {matching_precipitation}"  # noqa
                )
                break

    return is_good_weather_overall
