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
