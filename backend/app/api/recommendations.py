from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, DbSession, get_places_service, get_recommendation_service
from app.database.session import get_db
from app.models.favorite import Favorite
from app.models.visit import Visit
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.services.places_service import PlacesService
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

PlacesSvc = Annotated[PlacesService, Depends(get_places_service)]
RecSvc = Annotated[RecommendationService, Depends(get_recommendation_service)]


@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    body: RecommendationRequest,
    current_user: CurrentUser,
    db: DbSession,
    places: PlacesSvc,
    rec_service: RecSvc,
) -> RecommendationResponse:
    # Fetch nearby places
    raw_places = await places.search_nearby(body.lat, body.lng, body.radius_m, max_results=40)

    # If text mood provided, also search by text and merge
    if body.mood_text:
        text_results = await places.search_by_text(body.mood_text, body.lat, body.lng)
        seen_ids = {p.place_id for p in raw_places}
        for p in text_results:
            if p.place_id not in seen_ids:
                raw_places.append(p)
                seen_ids.add(p.place_id)

    # Load user context
    favs_result = await db.execute(
        select(Favorite).where(Favorite.user_id == current_user.id)
    )
    user_favorites = list(favs_result.scalars().all())

    visits_result = await db.execute(
        select(Visit).where(Visit.user_id == current_user.id)
    )
    user_visits = list(visits_result.scalars().all())

    recs = rec_service.rank_recommendations(body, raw_places, user_favorites, user_visits)
    return RecommendationResponse(recommendations=recs, total=len(recs))
