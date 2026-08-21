import pytest

@pytest.mark.asyncio
async def test_tenant_register_and_user_flow(client):
    resp = await client.post("/tenant/register", json={"name": "Test App", "email": "dev@test.com", "password": "Str0ngP@ss1"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    public_key = body["data"]["public_key"]

    resp = await client.post("/auth/register", json={"email": "user@test.com", "password": "Str0ngP@ss1"}, headers={"X-API-Key": public_key})
    assert resp.status_code == 200
    assert resp.json()["data"]["tokens"]["access_token"]

    resp = await client.post("/auth/login", json={"email": "user@test.com", "password": "Str0ngP@ss1"}, headers={"X-API-Key": public_key})
    assert resp.status_code == 200

    resp = await client.post("/auth/login", json={"email": "user@test.com", "password": "wrongpass"}, headers={"X-API-Key": public_key})
    assert resp.status_code == 401
    assert resp.json()["success"] is False

@pytest.mark.asyncio
async def test_health_endpoint(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "ok"
