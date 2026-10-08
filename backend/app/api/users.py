from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Response, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, DbSession, get_current_active_user
from app.database.session import get_db
from app.models.preference import Preference
from app.models.user import User
from app.schemas.preference import PreferenceResponse, UpdatePreferenceRequest
from app.schemas.user import UpdateUserRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser) -> User:
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_me(
    body: UpdateUserRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> User:
    if body.username is not None:
        existing = await db.execute(
            select(User).where(
                User.username == body.username.lower(),
                User.id != current_user.id,
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken",
            )
        current_user.username = body.username.lower()

    if body.display_name is not None:
        current_user.display_name = body.display_name

    if body.bio is not None:
        current_user.bio = body.bio

    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_me(current_user: CurrentUser, db: DbSession) -> None:
    current_user.is_deleted = True
    current_user.is_active = False
    await db.commit()


@router.get("/me/preferences", response_model=PreferenceResponse)
async def get_preferences(current_user: CurrentUser, db: DbSession) -> Preference:
    result = await db.execute(
        select(Preference).where(Preference.user_id == current_user.id)
    )
    pref = result.scalar_one_or_none()
    if pref is None:
        # Create default preferences if missing
        pref = Preference(user_id=current_user.id)
        db.add(pref)
        await db.commit()
        await db.refresh(pref)
    return pref


@router.put("/me/preferences", response_model=PreferenceResponse)
async def update_preferences(
    body: UpdatePreferenceRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> Preference:
    result = await db.execute(
        select(Preference).where(Preference.user_id == current_user.id)
    )
    pref = result.scalar_one_or_none()
    if pref is None:
        pref = Preference(user_id=current_user.id)
        db.add(pref)

    if body.preferred_vibes is not None:
        pref.preferred_vibes = body.preferred_vibes
    if body.preferred_max_distance_km is not None:
        pref.preferred_max_distance_km = body.preferred_max_distance_km
    if body.preferred_min_rating is not None:
        pref.preferred_min_rating = body.preferred_min_rating
    if body.onboarding_completed is not None:
        pref.onboarding_completed = body.onboarding_completed
    if body.location_permission_asked is not None:
        pref.location_permission_asked = body.location_permission_asked

    await db.commit()
    await db.refresh(pref)
    return pref


