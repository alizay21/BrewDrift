from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.schemas.place import Place, PlaceLocation
from app.schemas.recommendation import RecommendationRequest, RecommendationFilters
from app.services.mock_places_provider import MockPlacesProvider
from app.services.recommendation_service import RecommendationService

pytestmark = pytest.mark.asyncio

REC_PAYLOAD = {
    "lat": 51.5,
    "lng": -0.1,
    "selected_vibes": ["cozy", "bookish"],
    "radius_m": 2000,
    "filters": {},
}


async def test_recommendations_returns_list(client: AsyncClient, test_user, auth_headers) -> None:
    resp = await client.post("/recommendations/", headers=auth_headers, json=REC_PAYLOAD)
    assert resp.status_code == 200
    data = resp.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)


async def test_mock_provider_returns_places() -> None:
    provider = MockPlacesProvider()
    places = await provider.search_nearby(51.5, -0.1, 2000, 10)
    assert len(places) == 10
    assert all(p.name for p in places)


async def test_mock_text_search() -> None:
    provider = MockPlacesProvider()
    results = await provider.search_by_text("cozy", 51.5, -0.1)
    assert len(results) > 0


async def test_vibe_scoring_produces_scores() -> None:
    service = RecommendationService()
    place = Place(
        place_id="test_001",
        name="The Cozy Nook",
        location=PlaceLocation(lat=51.5, lng=-0.1),
        types=["cafe", "coffee_shop"],
        editorial_summary="A warm intimate corner cafe perfect for reading.",
        rating=4.7,
    )
    scores = service.score_vibe_match(place, ["cozy", "caffeinated"])
    assert "cozy" in scores
    assert "caffeinated" in scores
    assert scores["cozy"].score > 0
    assert scores["caffeinated"].confidence in ("high", "medium", "low")


async def test_recommendation_ranking_orders_by_score() -> None:
    service = RecommendationService()
    provider = MockPlacesProvider()
    places = await provider.search_nearby(51.5, -0.1, 5000, 10)

    request = RecommendationRequest(
        lat=51.5,
        lng=-0.1,
        selected_vibes=["cozy"],
        radius_m=5000,
        filters=RecommendationFilters(),
    )
    recs = service.rank_recommendations(request, places, [], [])
    assert len(recs) > 0
    scores = [r.overall_score for r in recs]
    assert scores == sorted(scores, reverse=True)
