async def _try_ipapi(ip: str) -> str | None:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{settings.ipapi_url}/{ip}/json/")
            if resp.status_code == 200:
                data = resp.json()
                if data.get("error"):
                    return None
                city = data.get("city")
                country = data.get("country_name")
                if city and country:
                    return f"{city}, {country}"
                return country
    except Exception:
        pass
    return None

async def _try_ip_api_com(ip: str) -> str | None:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"http://ip-api.com/json/{ip}")
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "success":
                    city = data.get("city", "")
                    country = data.get("country", "")
                    return f"{city}, {country}".strip(", ") or None
    except Exception:
        pass
    return None

async def _try_ipgeolocation_io(ip: str) -> str | None:
    if not settings.ipgeolocation_api_key:
        return None
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(
                "https://api.ipgeolocation.io/ipgeo",
                params={"apiKey": settings.ipgeolocation_api_key, "ip": ip},
            )
            if resp.status_code == 200:
                data = resp.json()
                city = data.get("city")
                country = data.get("country_name")
                if city and country:
                    return f"{city}, {country}"
                return country
    except Exception:
        pass
    return None

GEOIP_CHAIN = [_try_ipapi, _try_ip_api_com, _try_ipgeolocation_io]

async def get_location_from_ip(ip_address: str) -> str:
    if not ip_address or ip_address in ("127.0.0.1", "localhost", "testclient"):
        return "Local/Unknown"

    for provider_fn in GEOIP_CHAIN:
        result = await provider_fn(ip_address)
        if result:
            return result

    return "Unknown"