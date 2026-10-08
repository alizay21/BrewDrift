from __future__ import annotations

from fastapi import APIRouter, Response, HTTPException, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession
from app.models.visit import Visit
from app.schemas.visit import CreateVisitRequest, UpdateVisitRequest, VisitResponse

router = APIRouter(prefix="/visits", tags=["visits"])


@router.get("/", response_model=list[VisitResponse])
async def list_visits(current_user: CurrentUser, db: DbSession) -> list[Visit]:
    result = await db.execute(
        select(Visit).where(Visit.user_id == current_user.id)
        .order_by(Visit.visited_at.desc())
    )
    return list(result.scalars().all())


@router.post("/", response_model=VisitResponse, status_code=status.HTTP_201_CREATED)
async def create_visit(
    body: CreateVisitRequest, current_user: CurrentUser, db: DbSession
) -> Visit:
    # Check duplicate
    existing = await db.execute(
        select(Visit).where(
            Visit.user_id == current_user.id,
            Visit.provider == body.provider,
            Visit.provider_place_id == body.provider_place_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already recorded a visit to this place",
        )

    visit = Visit(
        user_id=current_user.id,
        provider=body.provider,
        provider_place_id=body.provider_place_id,
        place_name_snapshot=body.place_name_snapshot,
        latitude=body.latitude,
        longitude=body.longitude,
        visited_at=body.visited_at,
    )
    db.add(visit)
    await db.commit()
    await db.refresh(visit)
    return visit


@router.get("/{visit_id}", response_model=VisitResponse)
async def get_visit(visit_id: str, current_user: CurrentUser, db: DbSession) -> Visit:
    result = await db.execute(
        select(Visit).where(Visit.id == visit_id, Visit.user_id == current_user.id)
    )
    visit = result.scalar_one_or_none()
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    return visit


@router.patch("/{visit_id}", response_model=VisitResponse)
async def update_visit(
    visit_id: str, body: UpdateVisitRequest, current_user: CurrentUser, db: DbSession
) -> Visit:
    result = await db.execute(
        select(Visit).where(Visit.id == visit_id, Visit.user_id == current_user.id)
    )
    visit = result.scalar_one_or_none()
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")

    if body.visited_at is not None:
        visit.visited_at = body.visited_at

    await db.commit()
    await db.refresh(visit)
    return visit


@router.delete("/{visit_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_visit(visit_id: str, current_user: CurrentUser, db: DbSession) -> None:
    result = await db.execute(
        select(Visit).where(Visit.id == visit_id, Visit.user_id == current_user.id)
    )
    visit = result.scalar_one_or_none()
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    await db.delete(visit)
    await db.commit()


