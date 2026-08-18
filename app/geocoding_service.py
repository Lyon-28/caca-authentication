import httpx

NOMINATIM_BASE = "https://nominatim.openstreetmap.org"
HEADERS = {"User-Agent": "CacaAuth/1.0 (auth-as-a-service)"}

async def geocode_address(address: str) -> dict | None:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                f"{NOMINATIM_BASE}/search",
                params={"q": address, "format": "json", "limit": 1},
                headers=HEADERS,
            )
            if resp.status_code == 200:
                results = resp.json()
                if results:
                    r = results[0]
                    return {"lat": float(r["lat"]), "lon": float(r["lon"]), "display_name": r["display_name"]}
    except Exception:
        pass
    return None

async def reverse_geocode(lat: float, lon: float) -> dict | None:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                f"{NOMINATIM_BASE}/reverse",
                params={"lat": lat, "lon": lon, "format": "json"},
                headers=HEADERS,
            )
            if resp.status_code == 200:
                data = resp.json()
                if "address" in data:
                    return {"display_name": data.get("display_name"), "address": data["address"]}
    except Exception:
        pass
    return None