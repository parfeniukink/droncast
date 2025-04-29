import math

from src.config import (
    EARTH_RADIUS_IN_KM,
    KM_PER_ONE_LATITUDE_DEGREE,
    KM_PER_ONE_LONGITUDE_DEGREE,
    STEP_KM,
)


def generate_coordinates_within_radius(lat, lon, radius_km):
    """
    Generates coordinates within the specified radius around the center point.

    This function calculates coordinates in a square grid
    around the central point (lat, lon) and filters out those
    within the specified radius using the Haversine formula.

    Args:
    - lat (float): Latitude of the center point.
    - lon (float): Longitude of the center point.
    - radius_km (float): Radius in kilometers within which to
      generate coordinates.

    Returns:
    - list: List of tuples containing generated coordinates
        within the specified radius.

    The function performs the following steps:
    - Calculates the change in latitude (`delta_lat`) and
      longitude (`delta_lon`) for each step of distance
      (`STEP_KM`) in terms of kilometers.
    - Determines the number of steps in latitude (`lat_steps`) and
      longitude (`lon_steps`) from the central point based on the given radius.
    - Iterates over a latitude and longitude of steps around the center point
      to generate potential coordinates.
    - new coords are calculated for each step from the central point
    - For each potential coordinate, calculates the distance
      from the center point using the Haversine formula.
    - If the distance is within the specified radius,
      adds the coordinate to the result list.
    """
    coords = []

    delta_lat = STEP_KM / KM_PER_ONE_LATITUDE_DEGREE
    delta_lon = STEP_KM / (
        KM_PER_ONE_LONGITUDE_DEGREE * math.cos(math.radians(lat))
    )

    lat_steps = int(radius_km / STEP_KM)
    lon_steps = int(radius_km / STEP_KM)

    for dlat in range(-lat_steps, lat_steps + 1):
        for dlon in range(-lon_steps, lon_steps + 1):
            new_lat = lat + dlat * delta_lat
            new_lon = lon + dlon * delta_lon

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

    The function performs the following steps:
    - Converts the latitude and longitude of both points
      from degrees to radians.
    - Calculates the differences in latitude and longitude
      between the two points.
    - Applies the Haversine formula to compute the angular distance.
    - Calculates the angular distance in radians.
    - Multiplies the angular distance by the Earth's radius
      to obtain the actual distance.

    Args:
    - lat1 (float): Latitude of the first point in degrees.
    - lon1 (float): Longitude of the first point in degrees.
    - lat2 (float): Latitude of the second point in degrees.
    - lon2 (float): Longitude of the second point in degrees.

    Returns:
    - float: The distance between the two points in kilometers.
    """

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    lambda1 = math.radians(lon1)
    lambda2 = math.radians(lon2)

    d_phi = phi2 - phi1
    d_lambda = lambda2 - lambda1

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_IN_KM * c
