"""
Generator script - Batch 4: Services
"""
import os


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {path}")


# ──────────────────────────────────────────────────────────────
# app/services/places_service.py
# ──────────────────────────────────────────────────────────────
write("app/services/places_service.py", """\
from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.schemas.place import Place, PlacePhoto


@runtime_checkable
class PlacesProvider(Protocol):
    async def search_nearby(
        self,
        lat: float,
        lng: float,
        radius_m: int = 1500,
        max_results: int = 20,
    ) -> list[Place]: ...

    async def search_by_text(
        self,
        query: str,
        lat: float | None = None,
        lng: float | None = None,
    ) -> list[Place]: ...

    async def get_place_details(self, place_id: str) -> Place | None: ...

    async def get_place_photos(self, place_id: str) -> list[PlacePhoto]: ...


class PlacesService:
    \"\"\"Delegates all operations to the injected PlacesProvider.\"\"\"

    def __init__(self, provider: PlacesProvider) -> None:
        self._provider = provider

    async def search_nearby(
        self,
        lat: float,
        lng: float,
        radius_m: int = 1500,
        max_results: int = 20,
    ) -> list[Place]:
        return await self._provider.search_nearby(lat, lng, radius_m, max_results)

    async def search_by_text(
        self,
        query: str,
        lat: float | None = None,
        lng: float | None = None,
    ) -> list[Place]:
        return await self._provider.search_by_text(query, lat, lng)

    async def get_place_details(self, place_id: str) -> Place | None:
        return await self._provider.get_place_details(place_id)

    async def get_place_photos(self, place_id: str) -> list[PlacePhoto]:
        return await self._provider.get_place_photos(place_id)
""")

# ──────────────────────────────────────────────────────────────
# app/services/google_places_provider.py
# ──────────────────────────────────────────────────────────────
write("app/services/google_places_provider.py", """\
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
    \"\"\"Google Places API (New) provider using httpx.\"\"\"

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
""")

# ──────────────────────────────────────────────────────────────
# app/services/mock_places_provider.py
# ──────────────────────────────────────────────────────────────
write("app/services/mock_places_provider.py", """\
from __future__ import annotations

\"\"\"
MockPlacesProvider – returns realistic fake cafe/bar/bookshop data.

WARNING: This provider is for DEVELOPMENT / TESTING only.
It is NEVER used when USE_MOCK_PLACES=false in production settings.
\"\"\"

import math
import random

from app.schemas.place import (
    Place,
    PlaceLocation,
    PlaceOpeningHours,
    PlacePhoto,
)

_MOCK_PLACES: list[dict] = [
    {
        "place_id": "mock_001",
        "name": "The Cozy Nook",
        "lat_offset": 0.003,
        "lng_offset": 0.002,
        "address": "12 Elm Street, Oldtown",
        "rating": 4.7,
        "rating_count": 312,
        "types": ["cafe", "coffee_shop"],
        "price_level": "$",
        "phone": "+1-555-0101",
        "website": "https://thecozycook.example.com",
        "editorial_summary": "A warm, intimate corner cafe perfect for reading and remote work.",
        "open_now": True,
    },
    {
        "place_id": "mock_002",
        "name": "Bloom & Brew",
        "lat_offset": -0.005,
        "lng_offset": 0.004,
        "address": "45 Garden Lane, Midcity",
        "rating": 4.5,
        "rating_count": 189,
        "types": ["cafe", "florist"],
        "price_level": "$$",
        "phone": "+1-555-0102",
        "website": "https://bloomandbrew.example.com",
        "editorial_summary": "Specialty coffee surrounded by fresh flowers and botanical decor.",
        "open_now": True,
    },
    {
        "place_id": "mock_003",
        "name": "Chapter One Cafe",
        "lat_offset": 0.007,
        "lng_offset": -0.003,
        "address": "88 Bookshelf Blvd, Readington",
        "rating": 4.8,
        "rating_count": 560,
        "types": ["cafe", "book_store"],
        "price_level": "$",
        "phone": "+1-555-0103",
        "website": "https://chapteronecafe.example.com",
        "editorial_summary": "A beloved bookshop-cafe hybrid with curated shelves and pour-over coffee.",
        "open_now": True,
    },
    {
        "place_id": "mock_004",
        "name": "The Velvet Cup",
        "lat_offset": -0.002,
        "lng_offset": -0.006,
        "address": "3 Silk Road, Uptown",
        "rating": 4.3,
        "rating_count": 97,
        "types": ["cafe", "bar"],
        "price_level": "$$",
        "phone": "+1-555-0104",
        "website": None,
        "editorial_summary": "Cozy daytime cafe that transforms into a cocktail lounge after dark.",
        "open_now": False,
    },
    {
        "place_id": "mock_005",
        "name": "Morning Pages",
        "lat_offset": 0.001,
        "lng_offset": 0.008,
        "address": "21 Writer's Row, Artsville",
        "rating": 4.6,
        "rating_count": 241,
        "types": ["cafe", "art_gallery"],
        "price_level": "$",
        "phone": "+1-555-0105",
        "website": "https://morningpages.example.com",
        "editorial_summary": "Minimalist cafe with rotating local art exhibitions and single-origin espresso.",
        "open_now": True,
    },
    {
        "place_id": "mock_006",
        "name": "The Amber Kettle",
        "lat_offset": -0.008,
        "lng_offset": 0.001,
        "address": "67 Copper Lane, Westside",
        "rating": 4.4,
        "rating_count": 155,
        "types": ["cafe", "bakery"],
        "price_level": "$",
        "phone": "+1-555-0106",
        "website": "https://amberkettle.example.com",
        "editorial_summary": "Artisan bakery cafe renowned for its sourdough and house-blend tea.",
        "open_now": True,
    },
    {
        "place_id": "mock_007",
        "name": "Groundwork Social",
        "lat_offset": 0.006,
        "lng_offset": 0.006,
        "address": "100 Commons Ave, Downtown",
        "rating": 4.2,
        "rating_count": 88,
        "types": ["cafe", "coworking_space"],
        "price_level": "$$",
        "phone": "+1-555-0107",
        "website": "https://groundworksocial.example.com",
        "editorial_summary": "Community-driven co-working cafe with high-speed WiFi and farm-to-cup brews.",
        "open_now": True,
    },
    {
        "place_id": "mock_008",
        "name": "Drift & Sip",
        "lat_offset": -0.004,
        "lng_offset": -0.004,
        "address": "9 Harbor Walk, Portview",
        "rating": 4.9,
        "rating_count": 703,
        "types": ["cafe", "bar", "restaurant"],
        "price_level": "$$",
        "phone": "+1-555-0108",
        "website": "https://driftandsip.example.com",
        "editorial_summary": "Waterfront cafe-bar with panoramic views and a creative brunch menu.",
        "open_now": True,
    },
    {
        "place_id": "mock_009",
        "name": "Foxen Library Cafe",
        "lat_offset": 0.009,
        "lng_offset": -0.009,
        "address": "42 Stacks Street, Libraryville",
        "rating": 4.6,
        "rating_count": 330,
        "types": ["cafe", "library"],
        "price_level": "$",
        "phone": "+1-555-0109",
        "website": "https://foxenlibrary.example.com",
        "editorial_summary": "Hushed, elegant cafe inside a historic library building. Perfect for deep focus.",
        "open_now": False,
    },
    {
        "place_id": "mock_010",
        "name": "Sundial Roasters",
        "lat_offset": -0.006,
        "lng_offset": 0.007,
        "address": "77 Sun Street, Northend",
        "rating": 4.8,
        "rating_count": 415,
        "types": ["cafe", "coffee_shop", "bakery"],
        "price_level": "$",
        "phone": "+1-555-0110",
        "website": "https://sundialroasters.example.com",
        "editorial_summary": "Third-wave roastery with seasonal single-origins and house-made pastries.",
        "open_now": True,
    },
]


def _make_photo(place_id: str, idx: int) -> PlacePhoto:
    return PlacePhoto(
        photo_reference=f"mock_photo_{place_id}_{idx}",
        url=f"https://picsum.photos/seed/{place_id}_{idx}/800/600",
        width=800,
        height=600,
        attributions=["Mock Data"],
    )


def _build_place(data: dict, base_lat: float, base_lng: float) -> Place:
    return Place(
        place_id=data["place_id"],
        name=data["name"],
        location=PlaceLocation(
            lat=base_lat + data["lat_offset"],
            lng=base_lng + data["lng_offset"],
        ),
        address=data.get("address"),
        rating=data.get("rating"),
        rating_count=data.get("rating_count"),
        photos=[_make_photo(data["place_id"], i) for i in range(3)],
        opening_hours=PlaceOpeningHours(open_now=data.get("open_now")),
        types=data.get("types", []),
        price_level=data.get("price_level"),
        phone=data.get("phone"),
        website=data.get("website"),
        editorial_summary=data.get("editorial_summary"),
    )


class MockPlacesProvider:
    \"\"\"
    MOCK provider — returns static fake places offset from the caller's coordinates.
    Only used when USE_MOCK_PLACES=True (development / testing).
    \"\"\"

    async def search_nearby(
        self,
        lat: float,
        lng: float,
        radius_m: int = 1500,
        max_results: int = 20,
    ) -> list[Place]:
        places = [_build_place(d, lat, lng) for d in _MOCK_PLACES]
        return places[:max_results]

    async def search_by_text(
        self,
        query: str,
        lat: float | None = None,
        lng: float | None = None,
    ) -> list[Place]:
        base_lat = lat or 0.0
        base_lng = lng or 0.0
        q = query.lower()
        results = []
        for d in _MOCK_PLACES:
            if (
                q in d["name"].lower()
                or any(q in t for t in d.get("types", []))
                or (d.get("editorial_summary") and q in d["editorial_summary"].lower())
            ):
                results.append(_build_place(d, base_lat, base_lng))
        if not results:
            # Return all if no match, for demo purposes
            results = [_build_place(d, base_lat, base_lng) for d in _MOCK_PLACES]
        return results

    async def get_place_details(self, place_id: str) -> Place | None:
        for d in _MOCK_PLACES:
            if d["place_id"] == place_id:
                return _build_place(d, 0.0, 0.0)
        return None

    async def get_place_photos(self, place_id: str) -> list[PlacePhoto]:
        for d in _MOCK_PLACES:
            if d["place_id"] == place_id:
                return [_make_photo(place_id, i) for i in range(5)]
        return []
""")

# ──────────────────────────────────────────────────────────────
# app/services/recommendation_service.py
# ──────────────────────────────────────────────────────────────
write("app/services/recommendation_service.py", """\
from __future__ import annotations

import math
from dataclasses import dataclass, field

from app.models.favorite import Favorite
from app.models.visit import Visit
from app.schemas.place import Place, PlaceLocation
from app.schemas.recommendation import (
    PlaceRecommendation,
    RecommendationRequest,
    VibeScore,
)

# Vibe keyword mapping: vibe_id -> keywords to look for in place data
VIBE_KEYWORDS: dict[str, list[str]] = {
    "cozy": ["cozy", "cosy", "intimate", "warm", "snug", "nook", "quiet", "peaceful"],
    "lively": ["lively", "vibrant", "bustling", "social", "busy", "energetic"],
    "bookish": ["book", "library", "literary", "read", "shelf", "chapter"],
    "artsy": ["art", "gallery", "creative", "craft", "design", "studio", "exhibit"],
    "hipster": ["specialty", "third-wave", "roastery", "pour-over", "single-origin", "artisan"],
    "study": ["wifi", "cowork", "focus", "quiet", "laptop", "work"],
    "social": ["social", "community", "commons", "meeting", "chat"],
    "romantic": ["velvet", "intimate", "candle", "dim", "serene", "evening"],
    "outdoorsy": ["garden", "outdoor", "terrace", "patio", "park", "nature"],
    "foodie": ["brunch", "menu", "pastry", "bakery", "sourdough", "farm-to"],
    "caffeinated": ["coffee", "espresso", "brew", "roast", "latte", "cappuccino"],
    "trendy": ["modern", "minimal", "contemporary", "sleek", "new", "fresh"],
}

VIBE_TYPES: dict[str, list[str]] = {
    "bookish": ["book_store", "library"],
    "artsy": ["art_gallery", "museum"],
    "caffeinated": ["cafe", "coffee_shop"],
    "foodie": ["bakery", "restaurant", "meal_takeaway"],
    "social": ["bar", "restaurant"],
    "romantic": ["bar"],
    "lively": ["bar", "night_club", "restaurant"],
}


@dataclass
class RecommendationWeights:
    vibe: float = 0.40
    preference: float = 0.20
    distance: float = 0.15
    rating: float = 0.15
    history: float = 0.10


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(dlng / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


class RecommendationService:
    def __init__(self, weights: RecommendationWeights | None = None) -> None:
        self.weights = weights or RecommendationWeights()

    def score_vibe_match(
        self, place: Place, vibes: list[str]
    ) -> dict[str, VibeScore]:
        if not vibes:
            return {}

        # Build searchable text corpus from place data
        corpus = " ".join(
            filter(
                None,
                [
                    place.name.lower(),
                    (place.editorial_summary or "").lower(),
                    " ".join(place.types).lower(),
                    (place.address or "").lower(),
                ],
            )
        )

        scores: dict[str, VibeScore] = {}
        for vibe in vibes:
            vibe_id = vibe.lower()
            keywords = VIBE_KEYWORDS.get(vibe_id, [vibe_id])
            type_hints = VIBE_TYPES.get(vibe_id, [])
            evidence: list[str] = []
            keyword_hits = 0

            for kw in keywords:
                if kw in corpus:
                    keyword_hits += 1
                    if kw in place.name.lower():
                        evidence.append(f"Name suggests '{kw}'")
                    elif kw in (place.editorial_summary or "").lower():
                        evidence.append(f"Description mentions '{kw}'")

            type_hits = sum(1 for t in type_hints if t in place.types)
            if type_hits:
                evidence.append(f"Place type matches {vibe_id} category")

            raw_score = min(1.0, (keyword_hits * 0.25) + (type_hits * 0.35))

            if raw_score >= 0.70:
                confidence = "high"
            elif raw_score >= 0.40:
                confidence = "medium"
            else:
                confidence = "low"

            scores[vibe_id] = VibeScore(
                vibe_id=vibe_id,
                score=round(raw_score, 3),
                confidence=confidence,
                evidence=evidence[:4],
            )
        return scores

    def score_distance(
        self, place_location: PlaceLocation, user_lat: float, user_lng: float, max_radius_m: int
    ) -> float:
        dist_km = _haversine_km(
            user_lat, user_lng, place_location.lat, place_location.lng
        )
        max_km = max_radius_m / 1000.0
        if dist_km >= max_km:
            return 0.0
        return round(1.0 - (dist_km / max_km), 3)

    def score_rating(self, rating: float | None) -> float:
        if rating is None:
            return 0.3  # neutral
        return round(min(1.0, rating / 5.0), 3)

    def score_personal_history(
        self,
        place_id: str,
        provider: str,
        favorites: list[Favorite],
        visits: list[Visit],
    ) -> float:
        is_fav = any(
            f.provider_place_id == place_id and f.provider == provider for f in favorites
        )
        has_visit = any(
            v.provider_place_id == place_id and v.provider == provider for v in visits
        )
        score = 0.0
        if is_fav:
            score += 0.6
        if has_visit:
            score += 0.4
        return min(1.0, score)

    def filter_places(self, places: list[Place]) -> list[Place]:
        filtered = []
        for p in places:
            if not p.name or not p.location:
                continue
            if p.rating is not None and p.rating < 1.0:
                continue
            filtered.append(p)
        return filtered

    def score_place(
        self,
        place: Place,
        request: RecommendationRequest,
        user_favorites: list[Favorite],
        user_visits: list[Visit],
    ) -> PlaceRecommendation:
        w = self.weights
        vibe_scores = self.score_vibe_match(place, request.selected_vibes)

        # Average vibe score
        avg_vibe = (
            sum(v.score for v in vibe_scores.values()) / len(vibe_scores)
            if vibe_scores
            else 0.5
        )

        dist_score = self.score_distance(
            place.location, request.lat, request.lng, request.radius_m
        )
        rating_score = self.score_rating(place.rating)
        history_score = self.score_personal_history(
            place.place_id, "google", user_favorites, user_visits
        )

        # Preference: boost if matches min_rating filter
        pref_score = 0.5
        if request.filters.min_rating and place.rating:
            pref_score = 1.0 if place.rating >= request.filters.min_rating else 0.1

        overall = round(
            w.vibe * avg_vibe
            + w.preference * pref_score
            + w.distance * dist_score
            + w.rating * rating_score
            + w.history * history_score,
            4,
        )

        if overall >= 0.70:
            confidence = "high"
        elif overall >= 0.40:
            confidence = "medium"
        else:
            confidence = "low"

        evidence: list[str] = []
        if rating_score >= 0.8 and place.rating:
            evidence.append(f"Highly rated ({place.rating:.1f}★)")
        if dist_score >= 0.7:
            evidence.append("Close to your location")
        if history_score > 0:
            evidence.append("In your favorites or visited before")
        for vs in vibe_scores.values():
            evidence.extend(vs.evidence[:2])

        return PlaceRecommendation(
            place=place,
            vibe_scores=vibe_scores,
            overall_score=min(1.0, overall),
            confidence=confidence,
            evidence=list(dict.fromkeys(evidence))[:6],
        )

    def rank_recommendations(
        self,
        request: RecommendationRequest,
        places: list[Place],
        user_favorites: list[Favorite],
        user_visits: list[Visit],
    ) -> list[PlaceRecommendation]:
        filtered = self.filter_places(places)

        # Apply hard filters
        if request.filters.min_rating is not None:
            filtered = [
                p for p in filtered
                if p.rating is None or p.rating >= request.filters.min_rating
            ]
        if request.filters.open_now is True:
            filtered = [
                p for p in filtered
                if p.opening_hours and p.opening_hours.open_now is True
            ]

        recs = [
            self.score_place(p, request, user_favorites, user_visits)
            for p in filtered
        ]
        recs.sort(key=lambda r: r.overall_score, reverse=True)
        return recs
""")

# ──────────────────────────────────────────────────────────────
# app/services/storage_service.py
# ──────────────────────────────────────────────────────────────
write("app/services/storage_service.py", """\
from __future__ import annotations

import hashlib
import io
import logging
import os
import uuid
from pathlib import Path

import aiofiles
from PIL import Image

from app.core.config import settings

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


class StorageService:
    def __init__(self) -> None:
        self._base_path = Path(settings.LOCAL_STORAGE_PATH)
        self._base_path.mkdir(parents=True, exist_ok=True)

    def validate_image(self, file_bytes: bytes, mime_type: str) -> None:
        \"\"\"Validate MIME type, extension, and image integrity. Raises ValueError on failure.\"\"\"
        if mime_type not in ALLOWED_MIME_TYPES:
            raise ValueError(
                f"Unsupported MIME type '{mime_type}'. "
                f"Allowed: {', '.join(sorted(ALLOWED_MIME_TYPES))}"
            )
        if len(file_bytes) > settings.max_upload_bytes:
            raise ValueError(
                f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE_MB} MB."
            )
        try:
            img = Image.open(io.BytesIO(file_bytes))
            img.verify()
        except Exception as exc:
            raise ValueError(f"Invalid or corrupt image file: {exc}") from exc

    async def save_file(
        self, file_bytes: bytes, filename: str, mime_type: str
    ) -> str:
        \"\"\"Persist file to local storage and return the public URL path.\"\"\"
        # Generate a unique filename to avoid collisions
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            ext = ".jpg"
        unique_name = f"{uuid.uuid4().hex}{ext}"
        dest = self._base_path / unique_name

        async with aiofiles.open(dest, "wb") as fh:
            await fh.write(file_bytes)

        logger.info("Saved file: %s (%d bytes)", dest, len(file_bytes))
        return f"/uploads/{unique_name}"

    async def delete_file(self, url: str) -> bool:
        \"\"\"Delete a file by its URL path. Returns True on success.\"\"\"
        try:
            filename = url.split("/")[-1]
            dest = self._base_path / filename
            if dest.exists():
                dest.unlink()
                logger.info("Deleted file: %s", dest)
                return True
            return False
        except Exception as exc:
            logger.error("Failed to delete file %s: %s", url, exc)
            return False
""")

print("\nBatch 4 complete: all services written")
