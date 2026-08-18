from fastapi import APIRouter, Query
from app.geocoding_service import geocode_address, reverse_geocode

router = APIRouter(prefix="/geocoding", tags=["Geocoding"])

@router.get("/search")
async def search_address(q: str = Query(..., min_length=3)):
    result = await geocode_address(q)
    return {"success": True, "data": result, "meta": {"provider": "nominatim"}}

@router.get("/reverse")
async def reverse_lookup(lat: float, lon: float):
    result = await reverse_geocode(lat, lon)
    return {"success": True, "data": result, "meta": {"provider": "nominatim"}}