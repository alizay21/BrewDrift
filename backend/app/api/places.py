from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import CurrentUser, get_places_service
from app.schemas.place import (
    NearbyPlacesResponse,
    Place,
    PlacePhoto,
    SearchPlacesResponse,
)
from app.services.places_service import PlacesService

router = APIRouter(prefix="/places", tags=["places"])

PlacesSvc = Annotated[PlacesService, Depends(get_places_service)]


@router.get("/nearby", response_model=NearbyPlacesResponse)
async def get_nearby_places(
    _: CurrentUser,
    places: PlacesSvc,
    lat: float = Query(ge=-90, le=90),
    lng: float = Query(ge=-180, le=180),
    radius_m: int = Query(default=1500, ge=1, le=50000),
    max_results: int = Query(default=20, ge=1, le=50),
) -> NearbyPlacesResponse:
    results = await places.search_nearby(lat, lng, radius_m, max_results)
    return NearbyPlacesResponse(places=results, total=len(results))


@router.get("/search", response_model=SearchPlacesResponse)
async def search_places(
    _: CurrentUser,
    places: PlacesSvc,
    q: str = Query(min_length=1, max_length=200),
    lat: float | None = Query(default=None, ge=-90, le=90),
    lng: float | None = Query(default=None, ge=-180, le=180),
) -> SearchPlacesResponse:
    results = await places.search_by_text(q, lat, lng)
    return SearchPlacesResponse(places=results, total=len(results))


@router.get("/{place_id}", response_model=Place)
async def get_place_detail(
    place_id: str,
    _: CurrentUser,
    places: PlacesSvc,
) -> Place:
    place = await places.get_place_details(place_id)
    if place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    return place


@router.get("/{place_id}/photos", response_model=list[PlacePhoto])
async def get_place_photos(
    place_id: str,
    _: CurrentUser,
    places: PlacesSvc,
) -> list[PlacePhoto]:
    return await places.get_place_photos(place_id)
