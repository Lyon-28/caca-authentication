<div align="center">

# 🔐 Caca Auth API

### Production-ready Authentication & Authorization API

<p>
  <img src="https://img.shields.io/badge/status-production-brightgreen?style=for-the-badge" alt="status" />
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge" alt="version" />
  <img src="https://img.shields.io/badge/license-MIT-informational?style=for-the-badge" alt="license" />
</p>

**Base URL:** `https://caca-authentication.vercel.app`

</div>

---

## 📚 Daftar Isi

<table>
<tr>
<td width="33%" valign="top">

- [🔑 Autentikasi](#-autentikasi)
- [🏢 Tenant](#1-tenant)
- [👤 Auth](#2-auth-end-user-butuh-x-api-key)
- [✉️ Passwordless](#3-passwordless)

</td>
<td width="33%" valign="top">

- [📱 Session](#4-session)
- [🌐 OAuth](#5-oauth)
- [🙍 Profile](#6-profile)
- [🛡️ MFA/TOTP](#7-mfa--totp)

</td>
<td width="33%" valign="top">

- [📊 Metrics](#8-metrics)
- [❤️ Health](#9-health)
- [📄 Terms](#10-terms)
- [👮 Admin](#11-admin)
- [🗺️ Geocoding](#12-geocoding)

</td>
</tr>
</table>

---

## 🔑 Autentikasi

Ada dua jenis header otorisasi yang digunakan di seluruh API ini:

| Header | Digunakan di | Contoh |
|---|---|---|
| `X-API-Key` | Endpoint publik `/auth/*` (register, login, OTP, magic link, OAuth start, metrics) | `X-API-Key: YOUR_API_KEY` |
| `Authorization` | Endpoint yang butuh login user/tenant/admin | `Authorization: Bearer <access_token>` |

> ⚠️ **Penting:** Beberapa contoh kode dari ReDoc *tidak* menampilkan header `Authorization` meski field-nya wajib di schema (misalnya `/profile/avatar`, `/profile/deactivate`, `/auth/change-password`). Ini bug dokumentasi bawaan — tetap sertakan header tersebut.

---

## 1. TENANT

Endpoint untuk pemilik proyek/API key.

### `POST` /tenant/register

Mendaftarkan tenant baru.

<details>
<summary><b>📦 Lihat contoh kode</b></summary>

**cURL**
```bash
curl -X POST "https://caca-authentication.vercel.app/tenant/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "string", "email": "string", "password": "string"}'
```

**JavaScript**
```js
const response = await fetch("https://caca-authentication.vercel.app/tenant/register", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "string", email: "string", password: "string" })
});
const data = await response.json();
```

**Python**
```python
import requests
requests.post("https://caca-authentication.vercel.app/tenant/register",
    json={"name": "string", "email": "string", "password": "string"}).json()
```

**PHP**
```php
$ch = curl_init("https://caca-authentication.vercel.app/tenant/register");
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(["name"=>"string","email"=>"string","password"=>"string"]));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$data = json_decode(curl_exec($ch), true);
```

</details>

---

### `POST` /tenant/login

**Body:** `{email, password}` → menghasilkan token tenant.

<details>
<summary><b>📦 Lihat contoh kode</b></summary>

```bash
curl -X POST "https://caca-authentication.vercel.app/tenant/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "string", "password": "string"}'
```
```js
const { data } = await (await fetch(`${BASE}/tenant/login`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email, password })
})).json();
```
```python
r = requests.post(f"{BASE}/tenant/login", json={"email": email, "password": password}).json()
```
</details>

---

### `GET` 🔒 /tenant/dashboard

Butuh `Authorization`.

```bash
curl -X GET "https://caca-authentication.vercel.app/tenant/dashboard" \
  -H "Authorization: Bearer TENANT_TOKEN"
```

```js
await fetch(`${BASE}/tenant/dashboard`, { headers: { Authorization: `Bearer ${token}` } });
```
```python
requests.get(f"{BASE}/tenant/dashboard", headers={"Authorization": f"Bearer {token}"})
```

### `POST` 🔒 /tenant/regenerate-keys

Butuh `Authorization`. Regenerasi API key tenant.

```bash
curl -X POST "https://caca-authentication.vercel.app/tenant/regenerate-keys" \
  -H "Authorization: Bearer TENANT_TOKEN"
```

### `POST` 🔒 /tenant/logout

Butuh `Authorization`.

```bash
curl -X POST "https://caca-authentication.vercel.app/tenant/logout" \
  -H "Authorization: Bearer TENANT_TOKEN"
```

### `POST` 🔒 /tenant/newsletter/send

Butuh `Authorization`. **Body:** `{subject, body, only_verified=true, respect_preferences=true}`

```bash
curl -X POST "https://caca-authentication.vercel.app/tenant/newsletter/send" \
  -H "Authorization: Bearer TENANT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"subject":"Hi","body":"Konten","only_verified":true,"respect_preferences":true}'
```

### `GET` 🔒 /tenant/newsletter/preview-recipients

Butuh `Authorization`. **Query:** `only_verified`, `respect_preferences`.

```bash
curl -X GET "https://caca-authentication.vercel.app/tenant/newsletter/preview-recipients?only_verified=true&respect_preferences=true" \
  -H "Authorization: Bearer TENANT_TOKEN"
```

---

## 2. AUTH (end-user, butuh X-API-Key)

### `POST` /auth/register

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/register" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"string","password":"string"}'
```
```js
await fetch(`${BASE}/auth/register`, {
  method: "POST",
  headers: { "Content-Type": "application/json", "X-API-Key": API_KEY },
  body: JSON.stringify({ email, password })
});
```
```python
requests.post(f"{BASE}/auth/register", headers={"X-API-Key": API_KEY},
    json={"email": email, "password": password})
```

### `POST` /auth/login

Sama seperti register, response berisi `access_token` + `refresh_token`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/login" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"string","password":"string"}'
```

### `POST` /auth/refresh

> ⚠️ **Query param (bukan body!):** `refresh_token`. Header: `X-API-Key`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/refresh?refresh_token=TOKEN" \
  -H "X-API-Key: YOUR_API_KEY"
```
```js
await fetch(`${BASE}/auth/refresh?refresh_token=${refreshToken}`, {
  method: "POST",
  headers: { "X-API-Key": API_KEY }
});
```
```python
requests.post(f"{BASE}/auth/refresh", params={"refresh_token": refresh_token},
    headers={"X-API-Key": API_KEY})
```

### `GET` 🔒 /auth/me

Butuh `Authorization`.

```bash
curl -X GET "https://caca-authentication.vercel.app/auth/me" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

### `POST` /auth/verify-email

**Body:** `{token}`. Header: `X-API-Key`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/verify-email" \
  -H "X-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{"token":"string"}'
```

### `POST` /auth/resend-verification

**Body:** `{email}`. Header: `X-API-Key`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/resend-verification" \
  -H "X-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{"email":"string"}'
```

### `POST` /auth/forgot-password

**Body:** `{email}`. Header: `X-API-Key`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/forgot-password" \
  -H "X-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{"email":"string"}'
```

### `POST` /auth/reset-password

**Body:** `{token, new_password}`. Header: `X-API-Key`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/reset-password" \
  -H "X-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{"token":"string","new_password":"string"}'
```

### `POST` 🔒 /auth/change-password

Butuh `Authorization`. **Body:** `{old_password, new_password}`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/change-password" \
  -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"old_password":"string","new_password":"string"}'
```

### `POST` /auth/logout

**Body:** `{access_token, refresh_token}`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/logout" \
  -H "Content-Type: application/json" \
  -d '{"access_token":"string","refresh_token":"string"}'
```

### `POST` 🔒 /auth/logout-all

Butuh `Authorization`. Mencabut semua sesi.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/logout-all" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

---

## 3. PASSWORDLESS

### `POST` /auth/magic-link/request

**Body:** `{email}`. Header: `X-API-Key`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/magic-link/request" \
  -H "X-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{"email":"string"}'
```

### `POST` /auth/magic-link/verify

**Body:** `{token}`. Header: `X-API-Key`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/magic-link/verify" \
  -H "X-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{"token":"string"}'
```

### `POST` /auth/otp/request

**Body:** `{phone}`. Header: `X-API-Key`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/otp/request" \
  -H "X-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{"phone":"string"}'
```

### `POST` /auth/otp/verify

**Body:** `{phone, code}`. Header: `X-API-Key`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/otp/verify" \
  -H "X-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" \
  -d '{"phone":"string","code":"string"}'
```

### `POST` /auth/anonymous

Login tanpa kredensial. Header: `X-API-Key`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/anonymous" \
  -H "X-API-Key: YOUR_API_KEY"
```

---

## 4. SESSION

### `GET` 🔒 /auth/sessions

Butuh `Authorization`. Daftar sesi aktif user.

```bash
curl -X GET "https://caca-authentication.vercel.app/auth/sessions" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

### `DELETE` 🔒 /auth/sessions/{session_id}

Butuh `Authorization`.

```bash
curl -X DELETE "https://caca-authentication.vercel.app/auth/sessions/SESSION_ID" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

---

## 5. OAUTH

### `GET` /auth/oauth/{provider}/start

Header: `X-API-Key`. Redirect ke provider (`google`, `github`, dst).

```bash
curl -X GET "https://caca-authentication.vercel.app/auth/oauth/google/start" \
  -H "X-API-Key: YOUR_API_KEY"
```
```js
// biasanya dipakai untuk redirect browser, bukan fetch:
window.location.href = `${BASE}/auth/oauth/google/start?apiKey=${API_KEY}`;
```

### `GET` /auth/oauth/{provider}/callback

**Query:** `code`, `state`.

```bash
curl -X GET "https://caca-authentication.vercel.app/auth/oauth/google/callback?code=XXX&state=YYY"
```

### `POST` /auth/oauth/apple/callback

> ⚠️ Form-urlencoded (bukan JSON): `{code, state, user?}`.

```bash
curl -X POST "https://caca-authentication.vercel.app/auth/oauth/apple/callback" \
  -d "code=XXX&state=YYY&user=ZZZ"
```
```js
const form = new URLSearchParams({ code, state, user });
await fetch(`${BASE}/auth/oauth/apple/callback`, { method: "POST", body: form });
```
```python
requests.post(f"{BASE}/auth/oauth/apple/callback", data={"code": code, "state": state, "user": user})
```

---

## 6. PROFILE

> 🔒 Semua endpoint di section ini butuh `Authorization`.

### `PATCH` /profile

**Body:** `{name, bio, birth_date}`.

```bash
curl -X PATCH "https://caca-authentication.vercel.app/profile" \
  -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"string","bio":"string","birth_date":"string"}'
```

### `POST` /profile/avatar `multipart`

```bash
curl -X POST "https://caca-authentication.vercel.app/profile/avatar" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -F "file=@avatar.png"
```
```js
const form = new FormData();
form.append("file", fileInput.files[0]);
await fetch(`${BASE}/profile/avatar`, {
  method: "POST",
  headers: { Authorization: `Bearer ${token}` }, // JANGAN set Content-Type manual
  body: form
});
```
```python
files = {"file": open("avatar.png", "rb")}
requests.post(f"{BASE}/profile/avatar", headers={"Authorization": f"Bearer {token}"}, files=files)
```

### `DELETE` /profile/avatar

```bash
curl -X DELETE "https://caca-authentication.vercel.app/profile/avatar" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

### `POST` /profile/upload `multipart` (dokumen umum)

```bash
curl -X POST "https://caca-authentication.vercel.app/profile/upload" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -F "file=@dokumen.pdf"
```

### `GET` /profile/preferences

```bash
curl -X GET "https://caca-authentication.vercel.app/profile/preferences" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

### `PATCH` /profile/preferences

**Body:** `{language, timezone, notifications_enabled, privacy_profile_public}`.

```bash
curl -X PATCH "https://caca-authentication.vercel.app/profile/preferences" \
  -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"language":"id","timezone":"Asia/Jakarta","notifications_enabled":true,"privacy_profile_public":false}'
```

### `POST` /profile/change-email/request

**Body:** `{new_email}`.

```bash
curl -X POST "https://caca-authentication.vercel.app/profile/change-email/request" \
  -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"new_email":"string"}'
```

### `POST` /profile/change-email/confirm

**Body:** `{token}`.

```bash
curl -X POST "https://caca-authentication.vercel.app/profile/change-email/confirm" \
  -H "Content-Type: application/json" \
  -d '{"token":"string"}'
```

### `POST` /profile/deactivate

```bash
curl -X POST "https://caca-authentication.vercel.app/profile/deactivate" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

### `POST` /profile/reactivate

**Query:** `user_id`, `tenant_id`.

```bash
curl -X POST "https://caca-authentication.vercel.app/profile/reactivate?user_id=UID&tenant_id=TID"
```

### `DELETE` /profile/delete

**Query opsional:** `hard` (boolean, default `false`).

```bash
curl -X DELETE "https://caca-authentication.vercel.app/profile/delete?hard=false" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

---

## 7. MFA / TOTP

> 🔒 Semua endpoint di section ini butuh `Authorization`.

### `POST` /mfa/totp/setup

Menghasilkan secret/QR code.

```bash
curl -X POST "https://caca-authentication.vercel.app/mfa/totp/setup" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

### `POST` /mfa/totp/enable

**Body:** `{code}` (dari authenticator app).

```bash
curl -X POST "https://caca-authentication.vercel.app/mfa/totp/enable" \
  -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"code":"123456"}'
```

### `POST` /mfa/totp/verify

**Body:** `{code}`.

```bash
curl -X POST "https://caca-authentication.vercel.app/mfa/totp/verify" \
  -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"code":"123456"}'
```

### `POST` /mfa/totp/disable

**Body:** `{code}`.

```bash
curl -X POST "https://caca-authentication.vercel.app/mfa/totp/disable" \
  -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"code":"123456"}'
```

---

## 8. METRICS

> Header wajib: `X-API-Key`.

### `GET` /metrics/overview

```bash
curl -X GET "https://caca-authentication.vercel.app/metrics/overview" \
  -H "X-API-Key: YOUR_API_KEY"
```

### `GET` /metrics/auth-methods

```bash
curl -X GET "https://caca-authentication.vercel.app/metrics/auth-methods" \
  -H "X-API-Key: YOUR_API_KEY"
```

---

## 9. HEALTH

> 🌍 Publik, tanpa auth.

```bash
curl "https://caca-authentication.vercel.app/health"
curl "https://caca-authentication.vercel.app/health/db"
curl "https://caca-authentication.vercel.app/health/redis"
curl "https://caca-authentication.vercel.app/health/schema"
curl "https://caca-authentication.vercel.app/health/db-stats"
curl "https://caca-authentication.vercel.app/health/detailed"
```

---

## 10. TERMS

### `POST` /terms/versions

**Body:** `{version, content}`.

```bash
curl -X POST "https://caca-authentication.vercel.app/terms/versions" \
  -H "Content-Type: application/json" \
  -d '{"version":"1.0","content":"Isi terms..."}'
```

### `GET` /terms/latest

🌍 Publik.

```bash
curl "https://caca-authentication.vercel.app/terms/latest"
```

### `POST` 🔒 /terms/accept

Butuh `Authorization`. **Body:** `{version}`.

```bash
curl -X POST "https://caca-authentication.vercel.app/terms/accept" \
  -H "Authorization: Bearer ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"version":"1.0"}'
```

### `GET` 🔒 /terms/status

Butuh `Authorization`.

```bash
curl -X GET "https://caca-authentication.vercel.app/terms/status" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

---

## 11. ADMIN

> 🔒 Butuh `Authorization` admin.

### `POST` /admin/login

**Body:** `{email, password}`.

```bash
curl -X POST "https://caca-authentication.vercel.app/admin/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"string","password":"string"}'
```

### `POST` /admin/logout

```bash
curl -X POST "https://caca-authentication.vercel.app/admin/logout" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### `GET` /admin/users

**Query:** `tenant_id`, `page` (default `1`), `limit` (default `20`).

```bash
curl -X GET "https://caca-authentication.vercel.app/admin/users?page=1&limit=20" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### `POST` /admin/users/{user_id}/block

```bash
curl -X POST "https://caca-authentication.vercel.app/admin/users/USER_ID/block" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### `POST` /admin/users/{user_id}/unblock

```bash
curl -X POST "https://caca-authentication.vercel.app/admin/users/USER_ID/unblock" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### `POST` /admin/users/{user_id}/reset-mfa

```bash
curl -X POST "https://caca-authentication.vercel.app/admin/users/USER_ID/reset-mfa" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### `GET` /admin/tenants

```bash
curl -X GET "https://caca-authentication.vercel.app/admin/tenants" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### `GET` /admin/ip-rules

```bash
curl -X GET "https://caca-authentication.vercel.app/admin/ip-rules" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### `POST` /admin/ip-rules

**Body:** `{tenant_id, ip_address, rule_type, reason}`.

```bash
curl -X POST "https://caca-authentication.vercel.app/admin/ip-rules" \
  -H "Authorization: Bearer ADMIN_TOKEN" -H "Content-Type: application/json" \
  -d '{"tenant_id":"string","ip_address":"1.2.3.4","rule_type":"block","reason":"spam"}'
```

### `DELETE` /admin/ip-rules/{rule_id}

```bash
curl -X DELETE "https://caca-authentication.vercel.app/admin/ip-rules/RULE_ID" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### `GET` /admin/logs

**Query:** `user_id`, `limit` (default `50`).

```bash
curl -X GET "https://caca-authentication.vercel.app/admin/logs?limit=50" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

---

## 12. GEOCODING

> 🌍 Publik.

### `GET` /geocoding/search

**Query:** `q` (minimal 3 karakter).

```bash
curl "https://caca-authentication.vercel.app/geocoding/search?q=Jakarta"
```

### `GET` /geocoding/reverse

**Query:** `lat`, `lon`.

```bash
curl "https://caca-authentication.vercel.app/geocoding/reverse?lat=-6.2&lon=106.8"
```

---

## 13. ROOT

### `GET` /

```bash
curl "https://caca-authentication.vercel.app/"
```

---

## ⚠️ Catatan Penting

> 1. `refresh_token` di `/auth/refresh` adalah **query parameter**, bukan body JSON.
> 2. Upload file (`/profile/avatar`, `/profile/upload`) pakai `multipart/form-data` — jangan set header `Content-Type` manual di JS, biarkan browser yang isi boundary-nya.
> 3. `/auth/oauth/apple/callback` pakai `application/x-www-form-urlencoded`, bukan JSON.
> 4. Beberapa contoh kode bawaan ReDoc **tidak** menyertakan header `Authorization` walau field-nya wajib di schema (mis. `/profile/avatar`, `/profile/deactivate`, `/auth/change-password`) — itu bug dokumentasi. Tetap sertakan `Authorization` untuk endpoint yang butuh login.
> 5. Response sukses semuanya `200` dengan skema `{}` generik (tidak didefinisikan strict di OpenAPI) — bentuk pastinya perlu dites langsung.

---

<div align="center">

**Made with ❤️ for Caca Auth API**

</div>
