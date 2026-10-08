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
    await db.flush()
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
