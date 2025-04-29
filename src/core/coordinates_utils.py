import math

from src.core.constants import (
    EARTH_RADIUS_IN_KM,
    KM_PER_ONE_LATITUDE_DEGREE,
    KM_PER_ONE_LONGITUDE_DEGREE,
    STEP_KM,
)


# fmt: off
def generate_coordinates_within_radius(lat, lon, radius_km):
    """
    Generates coordinates within the specified radius around the center point.
    """
    coords = []

    delta_lat = STEP_KM / KM_PER_ONE_LATITUDE_DEGREE # latitude change per STEP_KM # noqa
    delta_lon = STEP_KM / (
        KM_PER_ONE_LONGITUDE_DEGREE * math.cos(math.radians(lat))
    )  # longitude change per STEP_KM

    lat_steps = int(radius_km / STEP_KM)  # number of steps for latitude for the given radius from the central point # noqa
    lon_steps = int(radius_km / STEP_KM)  # number of steps for longitude for the given radius from the central point # noqa

    for (dlat) in range(-lat_steps, lat_steps + 1):  # iterates over latitude steps, covering a square grid around the central point # noqa
        for (dlon) in range(-lon_steps, lon_steps + 1):  # iterates over longitude steps, covering a square grid around the central point # noqa
            new_lat = (lat + dlat * delta_lat)  # calculates the new latitude for each step from the central point # noqa
            new_lon = (lon + dlon * delta_lon)  # calculates the new longitude for each step from the central point # noqa

            # Calculate distance from center to the new point
            distance = haversine_distance(lat, lon, new_lat, new_lon)
            if distance <= radius_km:
                coords.append((new_lat, new_lon))

    return coords


# fmt: off
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two points on the Earth in kilometers.

    The Haversine formula is used to calculate the shortest distance
    over the Earth's surface taking into account its curvature.
    This formula assumes the Earth is a perfect sphere.
    """

    # Converts latitude and longitude from degrees to radians
    phi1 = math.radians(lat1)  # converts lat1 (latitude) to radians
    phi2 = math.radians(lat2)  # converts lat2 (latitude) to radians
    lambda1 = math.radians(lon1)  # converts lon1 (longitude) to radians
    lambda2 = math.radians(lon2)  # converts lon2 (longitude) to radians

    # Calculates the differences in latitude and longitude
    d_phi = phi2 - phi1  # difference in latitudes in radians
    d_lambda = lambda2 - lambda1  # difference in longitudes in radians

    # Apply Haversine formula
    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )

    # Calculates the angular distance in radians
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_IN_KM * c  # multiplies by Earth's radius to get actual distance # noqa
