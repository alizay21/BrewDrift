from __future__ import annotations

from fastapi import APIRouter, Response, HTTPException, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession
from app.models.favorite import Favorite
from app.schemas.favorite import CreateFavoriteRequest, FavoriteResponse

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("/", response_model=list[FavoriteResponse])
async def list_favorites(current_user: CurrentUser, db: DbSession) -> list[Favorite]:
    result = await db.execute(
        select(Favorite).where(Favorite.user_id == current_user.id)
        .order_by(Favorite.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite(
    body: CreateFavoriteRequest, current_user: CurrentUser, db: DbSession
) -> Favorite:
    # Check duplicate
    existing = await db.execute(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.provider == body.provider,
            Favorite.provider_place_id == body.provider_place_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Place already in favorites",
        )

    fav = Favorite(
        user_id=current_user.id,
        provider=body.provider,
        provider_place_id=body.provider_place_id,
    )
    db.add(fav)
    await db.commit()
    await db.refresh(fav)
    return fav


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def remove_favorite(
    favorite_id: str, current_user: CurrentUser, db: DbSession
) -> None:
    result = await db.execute(
        select(Favorite).where(Favorite.id == favorite_id)
    )
    fav = result.scalar_one_or_none()
    if fav is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
    if fav.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your favorite")
    await db.delete(fav)
    await db.commit()


