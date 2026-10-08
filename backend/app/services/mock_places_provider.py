from __future__ import annotations

"""
MockPlacesProvider – returns realistic fake cafe/bar/bookshop data.

WARNING: This provider is for DEVELOPMENT / TESTING only.
It is NEVER used when USE_MOCK_PLACES=false in production settings.
"""

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
    """
    MOCK provider — returns static fake places offset from the caller's coordinates.
    Only used when USE_MOCK_PLACES=True (development / testing).
    """

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
