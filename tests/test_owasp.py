import pytest

@pytest.mark.asyncio
async def test_weak_password_rejected(client):
    resp = await client.post("/tenant/register", json={"name": "T", "email": "a@test.com", "password": "weak"})
    assert resp.status_code == 422

@pytest.mark.asyncio
async def test_missing_api_key_rejected(client):
    resp = await client.post("/auth/register", json={"email": "u@test.com", "password": "Str0ngP@ss1"})
    assert resp.status_code == 422

@pytest.mark.asyncio
async def test_invalid_api_key_rejected(client):
    resp = await client.post("/auth/register", json={"email": "u@test.com", "password": "Str0ngP@ss1"}, headers={"X-API-Key": "caca-sk_invalid"})
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_sql_injection_login_safe(client):
    resp = await client.post("/tenant/login", json={"email": "' OR '1'='1", "password": "x"})
    assert resp.status_code in (401, 422)

@pytest.mark.asyncio
async def test_sql_injection_does_not_bypass_auth(client):
    tenant_resp = await client.post("/tenant/register", json={"name": "T", "email": "sqltest@test.com", "password": "Str0ngP@ss1"})
    secret_key = tenant_resp.json()["data"]["secret_key"]
    await client.post("/auth/register", json={"email": "victim@test.com", "password": "Str0ngP@ss1"}, headers={"X-API-Key": secret_key})

    resp = await client.post(
        "/auth/login",
        json={"email": "victim@test.com' --", "password": "anything"},
        headers={"X-API-Key": secret_key},
    )
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_no_credentials_no_access(client):
    resp = await client.get("/auth/me")
    assert resp.status_code == 422

@pytest.mark.asyncio
async def test_expired_or_garbage_token_rejected(client):
    resp = await client.get("/auth/me", headers={"Authorization": "Bearer garbage.token.here"})
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_user_token_cannot_access_admin_endpoints(client):
    tenant_resp = await client.post("/tenant/register", json={"name": "T", "email": "admintest@test.com", "password": "Str0ngP@ss1"})
    secret_key = tenant_resp.json()["data"]["secret_key"]
    user_resp = await client.post("/auth/register", json={"email": "normaluser@test.com", "password": "Str0ngP@ss1"}, headers={"X-API-Key": secret_key})
    user_access_token = user_resp.json()["data"]["tokens"]["access_token"]

    resp = await client.get("/admin/users", headers={"Authorization": f"Bearer {user_access_token}"})
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_tenant_token_cannot_access_user_endpoints(client):
    tenant_resp = await client.post("/tenant/register", json={"name": "T", "email": "crosstest@test.com", "password": "Str0ngP@ss1"})
    email = "crosstest@test.com"
    login_resp = await client.post("/tenant/login", json={"email": email, "password": "Str0ngP@ss1"})
    tenant_token = login_resp.json()["data"]["token"]

    resp = await client.get("/auth/me", headers={"Authorization": f"Bearer {tenant_token}"})
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_cross_tenant_data_isolation(client):
    tenant_a = await client.post("/tenant/register", json={"name": "A", "email": "tenanta@test.com", "password": "Str0ngP@ss1"})
    tenant_b = await client.post("/tenant/register", json={"name": "B", "email": "tenantb@test.com", "password": "Str0ngP@ss1"})
    key_a = tenant_a.json()["data"]["secret_key"]
    key_b = tenant_b.json()["data"]["secret_key"]

    await client.post("/auth/register", json={"email": "shared@test.com", "password": "Str0ngP@ss1"}, headers={"X-API-Key": key_a})

    resp = await client.post("/auth/login", json={"email": "shared@test.com", "password": "Str0ngP@ss1"}, headers={"X-API-Key": key_b})
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_account_lockout_after_failed_attempts(client):
    tenant_resp = await client.post("/tenant/register", json={"name": "T", "email": "lockouttest@test.com", "password": "Str0ngP@ss1"})
    secret_key = tenant_resp.json()["data"]["secret_key"]
    await client.post("/auth/register", json={"email": "lockedout@test.com", "password": "Str0ngP@ss1"}, headers={"X-API-Key": secret_key})

    for _ in range(5):
        await client.post("/auth/login", json={"email": "lockedout@test.com", "password": "wrongpass"}, headers={"X-API-Key": secret_key})

    resp = await client.post("/auth/login", json={"email": "lockedout@test.com", "password": "Str0ngP@ss1"}, headers={"X-API-Key": secret_key})
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "ACCOUNT_LOCKED"

@pytest.mark.asyncio
async def test_rate_limit_enforced_on_register(client):
    tenant_resp = await client.post("/tenant/register", json={"name": "T", "email": "ratelimit@test.com", "password": "Str0ngP@ss1"})
    secret_key = tenant_resp.json()["data"]["secret_key"]

    statuses = []
    for i in range(15):
        resp = await client.post("/auth/register", json={"email": f"rl{i}@test.com", "password": "Str0ngP@ss1"}, headers={"X-API-Key": secret_key})
        statuses.append(resp.status_code)

    assert 429 in statuses

@pytest.mark.asyncio
async def test_password_hash_never_exposed(client):
    tenant_resp = await client.post("/tenant/register", json={"name": "T", "email": "hashtest@test.com", "password": "Str0ngP@ss1"})
    secret_key = tenant_resp.json()["data"]["secret_key"]
    resp = await client.post("/auth/register", json={"email": "hashcheck@test.com", "password": "Str0ngP@ss1"}, headers={"X-API-Key": secret_key})
    body = resp.json()
    assert "password" not in str(body).lower() or "password_hash" not in str(body)

@pytest.mark.asyncio
async def test_reflected_input_not_executed(client):
    resp = await client.post(
        "/tenant/register",
        json={"name": "<script>alert(1)</script>", "email": "xsstest@test.com", "password": "Str0ngP@ss1"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["data"]["name"] == "<script>alert(1)</script>"

@pytest.mark.asyncio
async def test_error_responses_use_standard_envelope(client):
    resp = await client.post("/auth/login", json={"email": "notfound@test.com", "password": "x"}, headers={"X-API-Key": "caca-sk_invalid"})
    body = resp.json()
    assert body["success"] is False
    assert "code" in body["error"]
    assert "message" in body["error"]