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
    """Delegates all operations to the injected PlacesProvider."""

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
