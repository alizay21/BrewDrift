from __future__ import annotations

from pydantic import BaseModel, Field


class PlaceLocation(BaseModel):
    lat: float
    lng: float


class PlacePhoto(BaseModel):
    photo_reference: str
    url: str | None = None
    width: int = 0
    height: int = 0
    attributions: list[str] = []


class PlaceOpeningHoursPeriodTime(BaseModel):
    day: int
    hour: int
    minute: int


class PlaceOpeningHoursPeriod(BaseModel):
    open: PlaceOpeningHoursPeriodTime | None = None
    close: PlaceOpeningHoursPeriodTime | None = None


class PlaceOpeningHours(BaseModel):
    open_now: bool | None = None
    periods: list[PlaceOpeningHoursPeriod] | None = None
    weekday_descriptions: list[str] | None = None


class Place(BaseModel):
    place_id: str
    name: str
    location: PlaceLocation
    address: str | None = None
    rating: float | None = None
    rating_count: int | None = None
    photos: list[PlacePhoto] = []
    opening_hours: PlaceOpeningHours | None = None
    types: list[str] = []
    price_level: str | None = None
    phone: str | None = None
    website: str | None = None
    editorial_summary: str | None = None


class NearbyPlacesRequest(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    radius_m: int = Field(default=1500, ge=1, le=50000)
    max_results: int = Field(default=20, ge=1, le=50)


class NearbyPlacesResponse(BaseModel):
    places: list[Place]
    total: int


class SearchPlacesRequest(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    lat: float | None = Field(default=None, ge=-90, le=90)
    lng: float | None = Field(default=None, ge=-180, le=180)


class SearchPlacesResponse(BaseModel):
    places: list[Place]
    total: int
