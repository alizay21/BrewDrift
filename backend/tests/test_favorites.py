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
