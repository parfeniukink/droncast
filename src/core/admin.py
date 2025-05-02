from celery.exceptions import CeleryError
from django.contrib import admin
from django.core.exceptions import ValidationError
from django_admin_geomap import ModelAdmin

from src.config.celery import app
from src.core.models import Point, WeatherCheckResult
from src.core.tasks import check_weather_for_location


class WeatherCheckResultInline(admin.TabularInline):
    model = WeatherCheckResult
    extra = 0


@admin.register(Point)
class PointAdmin(ModelAdmin):
    list_display = (
        "id",
        "latitude",
        "longitude",
        "radius",
        "flight_time",
        "created_by",
    )
    readonly_fields = ("created_by",)
    inlines = [WeatherCheckResultInline]

    geomap_field_longitude = "longitude"
    geomap_field_latitude = "latitude"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

        if not change:
            # Launch Celery task after creating a new Point
            check_weather_for_location.apply_async(
                kwargs={"location_id": obj.id},
                task_id=str(obj.id),
            )

    def delete_model(self, request, obj):
        try:
            app.control.terminate(str(obj.id))

        except CeleryError:
            raise ValidationError(
                "Could not cancel Weather forecast due to a Celery error."
            )

        super().delete_model(request, obj)
