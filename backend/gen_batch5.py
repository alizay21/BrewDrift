"""
Generator script - Batch 5: API deps + routers
"""
import os


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {path}")


# ──────────────────────────────────────────────────────────────
# app/api/deps.py
# ──────────────────────────────────────────────────────────────
write("app/api/deps.py", """\
from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import decode_token
from app.database.session import get_db
from app.models.user import User
from app.services.mock_places_provider import MockPlacesProvider
from app.services.google_places_provider import GooglePlacesProvider
from app.services.places_service import PlacesService
from app.services.recommendation_service import RecommendationService

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(credentials.credentials)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    result = await db.execute(select(User).where(User.id == user_id, User.is_deleted == False))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )
    return current_user


def get_places_service() -> PlacesService:
    if settings.USE_MOCK_PLACES:
        return PlacesService(MockPlacesProvider())
    return PlacesService(GooglePlacesProvider())


def get_recommendation_service() -> RecommendationService:
    return RecommendationService()


# Convenient type aliases
CurrentUser = Annotated[User, Depends(get_current_active_user)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
""")

# ──────────────────────────────────────────────────────────────
# app/api/auth.py
# ──────────────────────────────────────────────────────────────
write("app/api/auth.py", """\
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_reset_token,
    hash_password,
    verify_password,
)
from app.database.session import get_db
from app.models.password_reset import PasswordReset
from app.models.preference import Preference
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


def _make_token_response(user: User) -> TokenResponse:
    access = create_access_token({"sub": user.id})
    refresh = create_refresh_token({"sub": user.id})
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: DbSession) -> TokenResponse:
    # Check email uniqueness
    existing_email = await db.execute(
        select(User).where(User.email == body.email.lower())
    )
    if existing_email.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Check username uniqueness
    existing_username = await db.execute(
        select(User).where(User.username == body.username.lower())
    )
    if existing_username.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    user = User(
        email=body.email.lower(),
        password_hash=hash_password(body.password),
        display_name=body.display_name,
        username=body.username.lower(),
    )
    db.add(user)
    await db.flush()

    # Create default preferences
    pref = Preference(user_id=user.id)
    db.add(pref)

    await db.commit()
    await db.refresh(user)
    logger.info("New user registered: %s", user.id)
    return _make_token_response(user)


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: DbSession) -> TokenResponse:
    result = await db.execute(
        select(User).where(User.email == body.email.lower(), User.is_deleted == False)
    )
    user = result.scalar_one_or_none()

    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    return _make_token_response(user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(body: RefreshRequest, db: DbSession) -> TokenResponse:
    payload = decode_token(body.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user_id = payload.get("sub")
    result = await db.execute(
        select(User).where(User.id == user_id, User.is_deleted == False, User.is_active == True)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return _make_token_response(user)


@router.post("/logout", response_model=MessageResponse)
async def logout() -> MessageResponse:
    # With short-lived JWTs, logout is client-side (delete token).
    # For server-side invalidation, a token blacklist (Redis) would be added.
    return MessageResponse(message="Logged out successfully. Please discard your tokens.")


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(body: ForgotPasswordRequest, db: DbSession) -> MessageResponse:
    result = await db.execute(
        select(User).where(User.email == body.email.lower(), User.is_deleted == False)
    )
    user = result.scalar_one_or_none()

    # Always return the same message to avoid user enumeration
    generic_msg = (
        "If that email is registered, a password reset link has been sent."
    )

    if user is None:
        return MessageResponse(message=generic_msg)

    raw_token, token_hash = generate_reset_token()
    reset = PasswordReset(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    db.add(reset)
    await db.commit()

    if settings.FORGOT_PASSWORD_DEV_MODE:
        logger.warning(
            "[DEV MODE] Password reset token for %s: %s", user.email, raw_token
        )
        return MessageResponse(
            message=f"[DEV MODE] Reset token: {raw_token}  (expires in 1 hour)"
        )

    # Production: send email here
    logger.info("Password reset requested for user %s", user.id)
    return MessageResponse(message=generic_msg)


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(body: ResetPasswordRequest, db: DbSession) -> MessageResponse:
    from app.core.security import hash_token

    token_hash = hash_token(body.token)
    now = datetime.now(timezone.utc)

    result = await db.execute(
        select(PasswordReset).where(
            PasswordReset.token_hash == token_hash,
            PasswordReset.used_at == None,
            PasswordReset.expires_at > now,
        )
    )
    reset = result.scalar_one_or_none()
    if reset is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    user_result = await db.execute(select(User).where(User.id == reset.user_id))
    user = user_result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    user.password_hash = hash_password(body.new_password)
    reset.used_at = now
    await db.commit()

    return MessageResponse(message="Password reset successfully.")
""")

# ──────────────────────────────────────────────────────────────
# app/api/users.py
# ──────────────────────────────────────────────────────────────
write("app/api/users.py", """\
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
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


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
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
""")

# ──────────────────────────────────────────────────────────────
# app/api/places.py
# ──────────────────────────────────────────────────────────────
write("app/api/places.py", """\
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
""")

# ──────────────────────────────────────────────────────────────
# app/api/recommendations.py
# ──────────────────────────────────────────────────────────────
write("app/api/recommendations.py", """\
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
""")

# ──────────────────────────────────────────────────────────────
# app/api/favorites.py
# ──────────────────────────────────────────────────────────────
write("app/api/favorites.py", """\
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
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


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
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
""")

# ──────────────────────────────────────────────────────────────
# app/api/visits.py
# ──────────────────────────────────────────────────────────────
write("app/api/visits.py", """\
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
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


@router.delete("/{visit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_visit(visit_id: str, current_user: CurrentUser, db: DbSession) -> None:
    result = await db.execute(
        select(Visit).where(Visit.id == visit_id, Visit.user_id == current_user.id)
    )
    visit = result.scalar_one_or_none()
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    await db.delete(visit)
    await db.commit()
""")

# ──────────────────────────────────────────────────────────────
# app/api/reviews.py
# ──────────────────────────────────────────────────────────────
write("app/api/reviews.py", """\
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentUser, DbSession
from app.models.review import Review
from app.models.visit import Visit
from app.schemas.review import CreateReviewRequest, ReviewResponse, UpdateReviewRequest

router = APIRouter(tags=["reviews"])


def _check_visit_ownership(visit: Visit | None, user_id: str) -> Visit:
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    if visit.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your visit")
    return visit


@router.get("/visits/{visit_id}/review", response_model=ReviewResponse)
async def get_review_for_visit(
    visit_id: str, current_user: CurrentUser, db: DbSession
) -> Review:
    visit_result = await db.execute(
        select(Visit).where(Visit.id == visit_id)
    )
    _check_visit_ownership(visit_result.scalar_one_or_none(), current_user.id)

    result = await db.execute(
        select(Review)
        .where(Review.visited_place_id == visit_id)
        .options(selectinload(Review.photos))
    )
    review = result.scalar_one_or_none()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review


@router.post(
    "/visits/{visit_id}/review",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    visit_id: str,
    body: CreateReviewRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> Review:
    visit_result = await db.execute(select(Visit).where(Visit.id == visit_id))
    _check_visit_ownership(visit_result.scalar_one_or_none(), current_user.id)

    # Check if review already exists
    existing = await db.execute(
        select(Review).where(Review.visited_place_id == visit_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Review already exists for this visit",
        )

    review = Review(
        user_id=current_user.id,
        visited_place_id=visit_id,
        personal_rating=body.personal_rating,
        experience_text=body.experience_text,
        personal_tags=body.personal_tags,
    )
    db.add(review)
    await db.commit()

    # Reload with photos
    result = await db.execute(
        select(Review)
        .where(Review.id == review.id)
        .options(selectinload(Review.photos))
    )
    return result.scalar_one()


@router.patch("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: str,
    body: UpdateReviewRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> Review:
    result = await db.execute(
        select(Review)
        .where(Review.id == review_id, Review.user_id == current_user.id)
        .options(selectinload(Review.photos))
    )
    review = result.scalar_one_or_none()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if body.personal_rating is not None:
        review.personal_rating = body.personal_rating
    if body.experience_text is not None:
        review.experience_text = body.experience_text
    if body.personal_tags is not None:
        review.personal_tags = body.personal_tags

    await db.commit()
    await db.refresh(review)
    result2 = await db.execute(
        select(Review).where(Review.id == review.id).options(selectinload(Review.photos))
    )
    return result2.scalar_one()


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: str, current_user: CurrentUser, db: DbSession
) -> None:
    result = await db.execute(
        select(Review).where(Review.id == review_id, Review.user_id == current_user.id)
    )
    review = result.scalar_one_or_none()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    await db.delete(review)
    await db.commit()
""")

# ──────────────────────────────────────────────────────────────
# app/api/photos.py
# ──────────────────────────────────────────────────────────────
write("app/api/photos.py", """\
from __future__ import annotations

import math

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentUser, DbSession
from app.core.config import settings
from app.models.photo import Photo
from app.models.review import Review
from app.schemas.review import PhotoResponse
from app.services.storage_service import StorageService

router = APIRouter(tags=["photos"])

MAX_PHOTOS_PER_REVIEW = 5


@router.post(
    "/reviews/{review_id}/photos",
    response_model=PhotoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_photo(
    review_id: str,
    current_user: CurrentUser,
    db: DbSession,
    file: UploadFile = File(...),
) -> Photo:
    # Verify review ownership
    result = await db.execute(
        select(Review).where(
            Review.id == review_id,
            Review.user_id == current_user.id,
        )
    )
    review = result.scalar_one_or_none()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    # Check photo count
    count_result = await db.execute(
        select(func.count()).where(Photo.review_id == review_id)
    )
    photo_count = count_result.scalar_one()
    if photo_count >= MAX_PHOTOS_PER_REVIEW:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Maximum {MAX_PHOTOS_PER_REVIEW} photos per review",
        )

    # Validate content-type header
    mime_type = file.content_type or "application/octet-stream"

    # Read file bytes
    file_bytes = await file.read()

    storage = StorageService()
    try:
        storage.validate_image(file_bytes, mime_type)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )

    url = await storage.save_file(file_bytes, file.filename or "upload.jpg", mime_type)

    photo = Photo(
        review_id=review_id,
        storage_url=url,
        filename=file.filename or "upload.jpg",
        mime_type=mime_type,
        file_size_kb=math.ceil(len(file_bytes) / 1024),
    )
    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo


@router.delete("/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(
    photo_id: str, current_user: CurrentUser, db: DbSession
) -> None:
    result = await db.execute(
        select(Photo)
        .where(Photo.id == photo_id)
        .options(selectinload(Photo.review))
    )
    photo = result.scalar_one_or_none()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    if photo.review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your photo")

    storage = StorageService()
    await storage.delete_file(photo.storage_url)

    await db.delete(photo)
    await db.commit()
""")

# ──────────────────────────────────────────────────────────────
# app/api/collections.py
# ──────────────────────────────────────────────────────────────
write("app/api/collections.py", """\
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentUser, DbSession
from app.models.collection import Collection
from app.models.collection_item import CollectionItem
from app.schemas.collection import (
    CollectionDetailResponse,
    CollectionItemRequest,
    CollectionItemResponse,
    CollectionResponse,
    CreateCollectionRequest,
    UpdateCollectionRequest,
)

router = APIRouter(prefix="/collections", tags=["collections"])


def _to_collection_response(col: Collection) -> CollectionResponse:
    return CollectionResponse(
        id=col.id,
        name=col.name,
        description=col.description,
        cover_photo_url=col.cover_photo_url,
        item_count=len(col.items),
        created_at=col.created_at,
        updated_at=col.updated_at,
    )


@router.get("/", response_model=list[CollectionResponse])
async def list_collections(current_user: CurrentUser, db: DbSession) -> list[CollectionResponse]:
    result = await db.execute(
        select(Collection)
        .where(Collection.user_id == current_user.id)
        .options(selectinload(Collection.items))
        .order_by(Collection.created_at.desc())
    )
    cols = result.scalars().all()
    return [_to_collection_response(c) for c in cols]


@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
async def create_collection(
    body: CreateCollectionRequest, current_user: CurrentUser, db: DbSession
) -> CollectionResponse:
    col = Collection(
        user_id=current_user.id,
        name=body.name,
        description=body.description,
    )
    db.add(col)
    await db.commit()
    await db.refresh(col)

    result = await db.execute(
        select(Collection).where(Collection.id == col.id).options(selectinload(Collection.items))
    )
    col = result.scalar_one()
    return _to_collection_response(col)


@router.get("/{collection_id}", response_model=CollectionDetailResponse)
async def get_collection(
    collection_id: str, current_user: CurrentUser, db: DbSession
) -> Collection:
    result = await db.execute(
        select(Collection)
        .where(Collection.id == collection_id, Collection.user_id == current_user.id)
        .options(selectinload(Collection.items))
    )
    col = result.scalar_one_or_none()
    if col is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    return col


@router.patch("/{collection_id}", response_model=CollectionResponse)
async def update_collection(
    collection_id: str,
    body: UpdateCollectionRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> CollectionResponse:
    result = await db.execute(
        select(Collection)
        .where(Collection.id == collection_id, Collection.user_id == current_user.id)
        .options(selectinload(Collection.items))
    )
    col = result.scalar_one_or_none()
    if col is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")

    if body.name is not None:
        col.name = body.name
    if body.description is not None:
        col.description = body.description

    await db.commit()
    await db.refresh(col)
    result2 = await db.execute(
        select(Collection).where(Collection.id == col.id).options(selectinload(Collection.items))
    )
    col = result2.scalar_one()
    return _to_collection_response(col)


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
    collection_id: str, current_user: CurrentUser, db: DbSession
) -> None:
    result = await db.execute(
        select(Collection).where(
            Collection.id == collection_id, Collection.user_id == current_user.id
        )
    )
    col = result.scalar_one_or_none()
    if col is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    await db.delete(col)
    await db.commit()


@router.post(
    "/{collection_id}/items",
    response_model=CollectionItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_collection_item(
    collection_id: str,
    body: CollectionItemRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> CollectionItem:
    col_result = await db.execute(
        select(Collection).where(
            Collection.id == collection_id, Collection.user_id == current_user.id
        )
    )
    if col_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")

    existing = await db.execute(
        select(CollectionItem).where(
            CollectionItem.collection_id == collection_id,
            CollectionItem.provider == body.provider,
            CollectionItem.provider_place_id == body.provider_place_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Place already in this collection",
        )

    item = CollectionItem(
        collection_id=collection_id,
        provider=body.provider,
        provider_place_id=body.provider_place_id,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{collection_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_collection_item(
    collection_id: str,
    item_id: str,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    col_result = await db.execute(
        select(Collection).where(
            Collection.id == collection_id, Collection.user_id == current_user.id
        )
    )
    if col_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")

    item_result = await db.execute(
        select(CollectionItem).where(
            CollectionItem.id == item_id,
            CollectionItem.collection_id == collection_id,
        )
    )
    item = item_result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    await db.delete(item)
    await db.commit()
""")

print("\nBatch 5 complete: all API routers written")
