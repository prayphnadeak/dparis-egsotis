"""GPS and geographic utilities for Kota Pagar Alam."""
from geopy.distance import geodesic
from typing import List, Tuple, TypeVar, Any

from app.core.constants import PAGAR_ALAM_BOUNDS


def is_within_pagar_alam(lat: float, lng: float) -> bool:
    """Check if a coordinate is within Pagar Alam bounding box."""
    b = PAGAR_ALAM_BOUNDS
    return b["min_lat"] <= lat <= b["max_lat"] and b["min_lng"] <= lng <= b["max_lng"]


def distance_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate straight-line distance in km between two GPS points."""
    return geodesic((lat1, lng1), (lat2, lng2)).km


def nearest(
    origin_lat: float,
    origin_lng: float,
    items: List[Any],
    lat_attr: str = "latitude",
    lng_attr: str = "longitude",
    limit: int = 5,
) -> List[Any]:
    """Return up to `limit` nearest items sorted by distance from origin."""
    def dist(item):
        lat = getattr(item, lat_attr, None)
        lng = getattr(item, lng_attr, None)
        if lat is None or lng is None:
            return float("inf")
        return distance_km(origin_lat, origin_lng, lat, lng)

    return sorted(items, key=dist)[:limit]


def google_maps_url(lat: float, lng: float) -> str:
    """Generate a Google Maps navigation URL."""
    return f"https://www.google.com/maps?q={lat},{lng}"
