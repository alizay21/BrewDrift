"""
Generator script - Batch 6: main.py + tests + alembic
"""
import os


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {path}")


# ──────────────────────────────────────────────────────────────
# app/main.py
# ──────────────────────────────────────────────────────────────
write("app/main.py", """\
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api import auth, collections, favorites, photos, places, recommendations, reviews, users
from app.core.config import settings
from app.database.session import create_tables

logging.basicConfig(
    level=logging.DEBUG if not settings.is_production else logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting Brewdrift API (env=%s)", settings.ENVIRONMENT)
    await create_tables()
    logger.info("Database tables verified/created")
    yield
    logger.info("Shutting down Brewdrift API")


app = FastAPI(
    title="Brewdrift API",
    description="Backend for the Brewdrift cafe-discovery app",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# ── CORS ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files (uploaded images) ──────────────────────────────
import os as _os
_os.makedirs(settings.LOCAL_STORAGE_PATH, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.LOCAL_STORAGE_PATH), name="uploads")

# ── Routers ─────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(places.router)
app.include_router(recommendations.router)
app.include_router(favorites.router)
app.include_router(visits.router)
app.include_router(reviews.router)
app.include_router(photos.router)
app.include_router(collections.router)


# ── Exception handlers ──────────────────────────────────────────
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception on %s %s: %s", request.method, request.url, exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


# ── Health check ────────────────────────────────────────────────
@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "use_mock_places": settings.USE_MOCK_PLACES,
    }
""")

# ──────────────────────────────────────────────────────────────
# tests/conftest.py
# ──────────────────────────────────────────────────────────────
write("tests/conftest.py", """\
from __future__ import annotations

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.security import create_access_token, hash_password
from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.models.user import User
from app.models.preference import Preference

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSessionLocal = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_tables():
    import app.models  # noqa: F401
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture()
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def test_user(db: AsyncSession) -> User:
    user = User(
        email="test@brewdrift.com",
        password_hash=hash_password("testpassword123"),
        display_name="Test User",
        username="testuser",
    )
    db.add(user)
    pref = Preference(user_id=user.id)
    db.add(pref)
    await db.commit()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture()
async def test_user2(db: AsyncSession) -> User:
    user = User(
        email="test2@brewdrift.com",
        password_hash=hash_password("testpassword123"),
        display_name="Test User 2",
        username="testuser2",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture()
def auth_headers(test_user: User) -> dict[str, str]:
    token = create_access_token({"sub": test_user.id})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def auth_headers2(test_user2: User) -> dict[str, str]:
    token = create_access_token({"sub": test_user2.id})
    return {"Authorization": f"Bearer {token}"}
""")

# ──────────────────────────────────────────────────────────────
# tests/test_auth.py
# ──────────────────────────────────────────────────────────────
write("tests/test_auth.py", """\
from __future__ import annotations

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_success(client: AsyncClient) -> None:
    resp = await client.post("/auth/register", json={
        "email": "newuser@test.com",
        "password": "securepass123",
        "display_name": "New User",
        "username": "newuser_reg",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_register_duplicate_email(client: AsyncClient) -> None:
    payload = {
        "email": "dup@test.com",
        "password": "securepass123",
        "display_name": "Dup",
        "username": "dup_user_email",
    }
    await client.post("/auth/register", json=payload)
    payload["username"] = "dup_user_email2"
    resp = await client.post("/auth/register", json=payload)
    assert resp.status_code == 409
    assert "Email" in resp.json()["detail"]


async def test_register_duplicate_username(client: AsyncClient) -> None:
    payload = {
        "email": "unique1@test.com",
        "password": "securepass123",
        "display_name": "U1",
        "username": "shared_username",
    }
    await client.post("/auth/register", json=payload)
    payload["email"] = "unique2@test.com"
    resp = await client.post("/auth/register", json=payload)
    assert resp.status_code == 409
    assert "Username" in resp.json()["detail"]


async def test_login_success(client: AsyncClient, test_user) -> None:
    resp = await client.post("/auth/login", json={
        "email": "test@brewdrift.com",
        "password": "testpassword123",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


async def test_login_wrong_password(client: AsyncClient, test_user) -> None:
    resp = await client.post("/auth/login", json={
        "email": "test@brewdrift.com",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401


async def test_login_nonexistent_user(client: AsyncClient) -> None:
    resp = await client.post("/auth/login", json={
        "email": "nobody@nowhere.com",
        "password": "whatever",
    })
    assert resp.status_code == 401


async def test_protected_without_token(client: AsyncClient) -> None:
    resp = await client.get("/users/me")
    assert resp.status_code == 401


async def test_token_refresh(client: AsyncClient, test_user) -> None:
    login_resp = await client.post("/auth/login", json={
        "email": "test@brewdrift.com",
        "password": "testpassword123",
    })
    refresh_token = login_resp.json()["refresh_token"]
    resp = await client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


async def test_refresh_with_access_token_fails(client: AsyncClient, test_user) -> None:
    from app.core.security import create_access_token
    token = create_access_token({"sub": test_user.id})
    resp = await client.post("/auth/refresh", json={"refresh_token": token})
    assert resp.status_code == 401
""")

# ──────────────────────────────────────────────────────────────
# tests/test_users.py
# ──────────────────────────────────────────────────────────────
write("tests/test_users.py", """\
from __future__ import annotations

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_get_current_user(client: AsyncClient, test_user, auth_headers) -> None:
    resp = await client.get("/users/me", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "test@brewdrift.com"
    assert data["username"] == "testuser"


async def test_update_profile(client: AsyncClient, test_user, auth_headers) -> None:
    resp = await client.patch(
        "/users/me",
        headers=auth_headers,
        json={"display_name": "Updated Name", "bio": "I love cafes"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["display_name"] == "Updated Name"
    assert data["bio"] == "I love cafes"


async def test_update_username_taken(client: AsyncClient, test_user, test_user2, auth_headers) -> None:
    resp = await client.patch(
        "/users/me",
        headers=auth_headers,
        json={"username": "testuser2"},
    )
    assert resp.status_code == 409


async def test_get_preferences(client: AsyncClient, test_user, auth_headers) -> None:
    resp = await client.get("/users/me/preferences", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "preferred_vibes" in data
    assert data["onboarding_completed"] is False


async def test_update_preferences(client: AsyncClient, test_user, auth_headers) -> None:
    resp = await client.put(
        "/users/me/preferences",
        headers=auth_headers,
        json={
            "preferred_vibes": ["cozy", "bookish"],
            "preferred_max_distance_km": 3,
            "preferred_min_rating": 4.0,
            "onboarding_completed": True,
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["preferred_vibes"] == ["cozy", "bookish"]
    assert data["onboarding_completed"] is True


async def test_delete_account(client: AsyncClient, db, auth_headers) -> None:
    from app.core.security import create_access_token, hash_password
    from app.models.user import User
    from app.models.preference import Preference
    user = User(
        email="todelete@test.com",
        password_hash=hash_password("pass123456"),
        display_name="Delete Me",
        username="deleteme_user",
    )
    db.add(user)
    pref = Preference(user_id=user.id)
    db.add(pref)
    await db.commit()
    await db.refresh(user)

    headers = {"Authorization": f"Bearer {create_access_token({'sub': user.id})}"}
    resp = await client.delete("/users/me", headers=headers)
    assert resp.status_code == 204

    # Subsequent request should 401
    resp2 = await client.get("/users/me", headers=headers)
    assert resp2.status_code == 401
""")

# ──────────────────────────────────────────────────────────────
# tests/test_favorites.py
# ──────────────────────────────────────────────────────────────
write("tests/test_favorites.py", """\
from __future__ import annotations

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

FAV_PAYLOAD = {"provider": "google", "provider_place_id": "mock_001"}


async def test_add_favorite(client: AsyncClient, test_user, auth_headers) -> None:
    resp = await client.post("/favorites/", headers=auth_headers, json=FAV_PAYLOAD)
    assert resp.status_code == 201
    assert resp.json()["provider_place_id"] == "mock_001"


async def test_list_favorites(client: AsyncClient, test_user, auth_headers) -> None:
    await client.post("/favorites/", headers=auth_headers, json=FAV_PAYLOAD)
    resp = await client.get("/favorites/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


async def test_add_duplicate_favorite(client: AsyncClient, test_user, auth_headers) -> None:
    await client.post("/favorites/", headers=auth_headers, json=FAV_PAYLOAD)
    resp = await client.post("/favorites/", headers=auth_headers, json=FAV_PAYLOAD)
    assert resp.status_code == 409


async def test_remove_favorite(client: AsyncClient, test_user, auth_headers) -> None:
    add_resp = await client.post("/favorites/", headers=auth_headers, json=FAV_PAYLOAD)
    fav_id = add_resp.json()["id"]
    del_resp = await client.delete(f"/favorites/{fav_id}", headers=auth_headers)
    assert del_resp.status_code == 204


async def test_cannot_remove_other_users_favorite(
    client: AsyncClient, test_user, test_user2, auth_headers, auth_headers2
) -> None:
    add_resp = await client.post("/favorites/", headers=auth_headers, json=FAV_PAYLOAD)
    fav_id = add_resp.json()["id"]
    del_resp = await client.delete(f"/favorites/{fav_id}", headers=auth_headers2)
    assert del_resp.status_code == 403
""")

# ──────────────────────────────────────────────────────────────
# tests/test_visits.py
# ──────────────────────────────────────────────────────────────
write("tests/test_visits.py", """\
from __future__ import annotations

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

VISIT_PAYLOAD = {
    "provider": "google",
    "provider_place_id": "mock_001",
    "place_name_snapshot": "The Cozy Nook",
    "latitude": 51.5,
    "longitude": -0.1,
    "visited_at": "2024-06-15T14:00:00Z",
}


async def test_create_visit(client: AsyncClient, test_user, auth_headers) -> None:
    resp = await client.post("/visits/", headers=auth_headers, json=VISIT_PAYLOAD)
    assert resp.status_code == 201
    data = resp.json()
    assert data["place_name_snapshot"] == "The Cozy Nook"


async def test_list_visits(client: AsyncClient, test_user, auth_headers) -> None:
    await client.post("/visits/", headers=auth_headers, json=VISIT_PAYLOAD)
    resp = await client.get("/visits/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


async def test_update_visit(client: AsyncClient, test_user, auth_headers) -> None:
    create_resp = await client.post("/visits/", headers=auth_headers, json=VISIT_PAYLOAD)
    visit_id = create_resp.json()["id"]
    resp = await client.patch(
        f"/visits/{visit_id}",
        headers=auth_headers,
        json={"visited_at": "2024-07-01T10:00:00Z"},
    )
    assert resp.status_code == 200
    assert "2024-07-01" in resp.json()["visited_at"]


async def test_delete_visit(client: AsyncClient, test_user, auth_headers) -> None:
    create_resp = await client.post("/visits/", headers=auth_headers, json=VISIT_PAYLOAD)
    visit_id = create_resp.json()["id"]
    resp = await client.delete(f"/visits/{visit_id}", headers=auth_headers)
    assert resp.status_code == 204


async def test_cross_user_isolation(
    client: AsyncClient, test_user, test_user2, auth_headers, auth_headers2
) -> None:
    create_resp = await client.post("/visits/", headers=auth_headers, json=VISIT_PAYLOAD)
    visit_id = create_resp.json()["id"]

    resp = await client.get(f"/visits/{visit_id}", headers=auth_headers2)
    assert resp.status_code == 404
""")

# ──────────────────────────────────────────────────────────────
# tests/test_recommendations.py
# ──────────────────────────────────────────────────────────────
write("tests/test_recommendations.py", """\
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
""")

print("\nBatch 6 complete: main.py + all tests written")
