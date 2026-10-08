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
