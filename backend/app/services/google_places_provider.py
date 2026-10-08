from __future__ import annotations

import logging
from typing import Any

import httpx

from app.core.config import settings
from app.schemas.place import (
    Place,
    PlaceLocation,
    PlaceOpeningHours,
    PlaceOpeningHoursPeriod,
    PlaceOpeningHoursPeriodTime,
    PlacePhoto,
)

logger = logging.getLogger(__name__)

_PLACES_BASE = "https://places.googleapis.com/v1"

_NEARBY_FIELD_MASK = (
    "places.id,places.displayName,places.location,places.formattedAddress,"
    "places.rating,places.userRatingCount,places.photos,places.currentOpeningHours,"
    "places.types,places.priceLevel,places.internationalPhoneNumber,places.websiteUri,"
    "places.editorialSummary"
)

_DETAIL_FIELD_MASK = (
    "id,displayName,location,formattedAddress,rating,userRatingCount,photos,"
    "currentOpeningHours,types,priceLevel,internationalPhoneNumber,websiteUri,editorialSummary"
)


def _map_price_level(raw: str | None) -> str | None:
    mapping = {
        "PRICE_LEVEL_FREE": "free",
        "PRICE_LEVEL_INEXPENSIVE": "$",
        "PRICE_LEVEL_MODERATE": "$$",
        "PRICE_LEVEL_EXPENSIVE": "$$$",
        "PRICE_LEVEL_VERY_EXPENSIVE": "$$$$",
    }
    return mapping.get(raw or "", None)


def _map_photo(raw: dict[str, Any], idx: int) -> PlacePhoto:
    name = raw.get("name", "")
    ref = name.split("/")[-1] if "/" in name else f"photo_{idx}"
    return PlacePhoto(
        photo_reference=name,
        url=f"https://places.googleapis.com/v1/{name}/media?maxWidthPx=800&key={settings.GOOGLE_PLACES_API_KEY}"
        if name
        else None,
        width=raw.get("widthPx", 0),
        height=raw.get("heightPx", 0),
        attributions=[a.get("displayName", "") for a in raw.get("authorAttributions", [])],
    )


def _map_period_time(raw: dict[str, Any] | None) -> PlaceOpeningHoursPeriodTime | None:
    if not raw:
        return None
    return PlaceOpeningHoursPeriodTime(
        day=raw.get("day", 0),
        hour=raw.get("hour", 0),
        minute=raw.get("minute", 0),
    )


def _map_opening_hours(raw: dict[str, Any] | None) -> PlaceOpeningHours | None:
    if not raw:
        return None
    periods = []
    for p in raw.get("periods", []):
        periods.append(
            PlaceOpeningHoursPeriod(
                open=_map_period_time(p.get("open")),
                close=_map_period_time(p.get("close")),
            )
        )
    return PlaceOpeningHours(
        open_now=raw.get("openNow"),
        periods=periods or None,
        weekday_descriptions=raw.get("weekdayDescriptions"),
    )


def _map_place(raw: dict[str, Any]) -> Place:
    loc = raw.get("location", {})
    display_name = raw.get("displayName", {})
    editorial = raw.get("editorialSummary", {})
    photos_raw = raw.get("photos", [])
    return Place(
        place_id=raw.get("id", raw.get("name", "unknown")),
        name=display_name.get("text", "Unknown") if isinstance(display_name, dict) else str(display_name),
        location=PlaceLocation(lat=loc.get("latitude", 0.0), lng=loc.get("longitude", 0.0)),
        address=raw.get("formattedAddress"),
        rating=raw.get("rating"),
        rating_count=raw.get("userRatingCount"),
        photos=[_map_photo(p, i) for i, p in enumerate(photos_raw[:5])],
        opening_hours=_map_opening_hours(raw.get("currentOpeningHours")),
        types=raw.get("types", []),
        price_level=_map_price_level(raw.get("priceLevel")),
        phone=raw.get("internationalPhoneNumber"),
        website=raw.get("websiteUri"),
        editorial_summary=editorial.get("text") if isinstance(editorial, dict) else None,
    )


class GooglePlacesProvider:
    """Google Places API (New) provider using httpx."""

    def __init__(self) -> None:
        self._api_key = settings.GOOGLE_PLACES_API_KEY
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=10.0)
        return self._client

    async def _post(self, path: str, body: dict, field_mask: str) -> dict[str, Any]:
        url = f"{_PLACES_BASE}{path}"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self._api_key,
            "X-Goog-FieldMask": field_mask,
        }
        resp = self._get_client().post(url, json=body, headers=headers)
        r = await resp
        r.raise_for_status()
        return r.json()

    async def _get(self, path: str, field_mask: str) -> dict[str, Any]:
        url = f"{_PLACES_BASE}{path}"
        headers = {
            "X-Goog-Api-Key": self._api_key,
            "X-Goog-FieldMask": field_mask,
        }
        r = await self._get_client().get(url, headers=headers)
        r.raise_for_status()
        return r.json()

    async def search_nearby(
        self,
        lat: float,
        lng: float,
        radius_m: int = 1500,
        max_results: int = 20,
    ) -> list[Place]:
        try:
            body = {
                "locationRestriction": {
                    "circle": {
                        "center": {"latitude": lat, "longitude": lng},
                        "radius": float(radius_m),
                    }
                },
                "maxResultCount": min(max_results, 20),
                "includedTypes": [
                    "cafe", "coffee_shop", "bar", "restaurant",
                    "bakery", "book_store", "library",
                ],
            }
            data = await self._post("/places:searchNearby", body, _NEARBY_FIELD_MASK)
            return [_map_place(p) for p in data.get("places", [])]
        except httpx.HTTPStatusError as exc:
            logger.error("Google Places nearby search failed: %s", exc.response.text)
            return []
        except Exception as exc:
            logger.error("Google Places nearby search error: %s", exc)
            return []

    async def search_by_text(
        self,
        query: str,
        lat: float | None = None,
        lng: float | None = None,
    ) -> list[Place]:
        try:
            body: dict[str, Any] = {"textQuery": query, "maxResultCount": 20}
            if lat is not None and lng is not None:
                body["locationBias"] = {
                    "circle": {
                        "center": {"latitude": lat, "longitude": lng},
                        "radius": 5000.0,
                    }
                }
            data = await self._post("/places:searchText", body, _NEARBY_FIELD_MASK)
            return [_map_place(p) for p in data.get("places", [])]
        except httpx.HTTPStatusError as exc:
            logger.error("Google Places text search failed: %s", exc.response.text)
            return []
        except Exception as exc:
            logger.error("Google Places text search error: %s", exc)
            return []

    async def get_place_details(self, place_id: str) -> Place | None:
        try:
            data = await self._get(f"/places/{place_id}", _DETAIL_FIELD_MASK)
            return _map_place(data)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            logger.error("Google Places detail fetch failed: %s", exc.response.text)
            return None
        except Exception as exc:
            logger.error("Google Places detail fetch error: %s", exc)
            return None

    async def get_place_photos(self, place_id: str) -> list[PlacePhoto]:
        place = await self.get_place_details(place_id)
        if place is None:
            return []
        return place.photos

    async def aclose(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
