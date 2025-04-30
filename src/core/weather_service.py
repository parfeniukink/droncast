from datetime import datetime

import requests
from django.conf import settings

from src.config import DATE_TIME_FORMAT


class WeatherForecastService:

    def precipitation_check(self, lat, lon, forecast_days, flight_time):
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&hourly=precipitation&daily=precipitation_sum"
            f"&forecast_days={forecast_days}&timezone=Europe/Kyiv"
        )

        response = requests.get(url)
        if response.status_code != 200:
            return None

        data = response.json()

        flight_time_str = flight_time.strftime(DATE_TIME_FORMAT)
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

        if (
            matching_precipitation is not None
            and matching_precipitation >= settings.DC_MAX_PRECIPITATION_MM
        ):
            print(
                f"!!! Bad weather! Big amount of precipitations!!! {matching_precipitation}"  # noqa
            )
            return False

        return True


weather_forecast_service = WeatherForecastService()
