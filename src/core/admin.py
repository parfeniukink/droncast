from django.contrib import admin

from src.core.models import WeatherLocation

from .tasks import check_weather_for_location


@admin.register(WeatherLocation)
class WeatherLocationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "latitude",
        "longitude",
        "radius",
        "flight_time",
        "created_by",
    )
    readonly_fields = ("created_by",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

        if not change:
            # Launch Celery task after creating a new WeatherLocation
            check_weather_for_location.apply_async(
                kwargs={"location_id": obj.id}
            )
