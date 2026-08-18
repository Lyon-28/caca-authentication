import os
import uuid
import base64
import httpx
from app.config import settings
from app.logging_config import logger

async def _try_supabase(file_bytes: bytes, filename: str, content_type: str) -> str | None:
    if not settings.supabase_url or not settings.supabase_service_key:
        return None
    try:
        path = f"{uuid.uuid4()}-{filename}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{settings.supabase_url}/storage/v1/object/{settings.supabase_storage_bucket}/{path}",
                headers={"Authorization": f"Bearer {settings.supabase_service_key}", "Content-Type": content_type},
                content=file_bytes,
            )
            if resp.status_code < 300:
                return f"{settings.supabase_url}/storage/v1/object/public/{settings.supabase_storage_bucket}/{path}"
    except Exception:
        pass
    return None

async def _try_imagekit(file_bytes: bytes, filename: str, content_type: str) -> str | None:
    if not settings.imagekit_private_key:
        return None
    try:
        async with httpx.AsyncClient(timeout=10.0, auth=(settings.imagekit_private_key, "")) as client:
            resp = await client.post(
                "https://upload.imagekit.io/api/v1/files/upload",
                data={"fileName": filename},
                files={"file": (filename, file_bytes, content_type)},
            )
            if resp.status_code < 300:
                return resp.json().get("url")
    except Exception:
        pass
    return None

async def _try_imgbb(file_bytes: bytes, filename: str, content_type: str) -> str | None:
    if not settings.imgbb_api_key:
        return None
    try:
        b64 = base64.b64encode(file_bytes).decode()
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                "https://api.imgbb.com/1/upload",
                data={"key": settings.imgbb_api_key, "image": b64, "name": filename},
            )
            if resp.status_code < 300:
                return resp.json().get("data", {}).get("url")
    except Exception:
        pass
    return None

async def _try_github(file_bytes: bytes, filename: str, content_type: str) -> str | None:
    if not settings.github_storage_token:
        return None
    try:
        b64 = base64.b64encode(file_bytes).decode()
        path = f"{uuid.uuid4()}-{filename}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.put(
                f"https://api.github.com/repos/{settings.github_storage_repo}/contents/{path}",
                headers={"Authorization": f"Bearer {settings.github_storage_token}"},
                json={"message": f"upload {path}", "content": b64},
            )
            if resp.status_code < 300:
                return resp.json().get("content", {}).get("download_url")
    except Exception:
        pass
    return None

async def _try_local(file_bytes: bytes, filename: str, content_type: str) -> str | None:
    try:
        os.makedirs(settings.local_storage_path, exist_ok=True)
        unique_name = f"{uuid.uuid4()}-{filename}"
        full_path = os.path.join(settings.local_storage_path, unique_name)
        with open(full_path, "wb") as f:
            f.write(file_bytes)
        return f"/static/uploads/{unique_name}"
    except Exception:
        return None

STORAGE_CHAIN = [_try_supabase, _try_imagekit, _try_imgbb, _try_github, _try_local]

async def upload_file(file_bytes: bytes, filename: str, content_type: str) -> str:
    for provider_fn in STORAGE_CHAIN:
        url = await provider_fn(file_bytes, filename, content_type)
        if url:
            return url
    raise RuntimeError("Semua storage provider gagal")
    
async def delete_file(url: str):
    if not url:
        return
    try:
        if "/static/uploads/" in url:
            filename = url.split("/static/uploads/")[-1]
            path = os.path.join(settings.local_storage_path, filename)
            if os.path.exists(path):
                os.remove(path)
            return

        if settings.supabase_url and settings.supabase_url in url:
            path = url.split(f"/{settings.supabase_storage_bucket}/")[-1]
            async with httpx.AsyncClient(timeout=10.0) as client:
                await client.delete(
                    f"{settings.supabase_url}/storage/v1/object/{settings.supabase_storage_bucket}/{path}",
                    headers={"Authorization": f"Bearer {settings.supabase_service_key}"},
                )
            return

        if settings.imagekit_url_endpoint and settings.imagekit_url_endpoint in url:
            file_id = url.split("/")[-1]
            async with httpx.AsyncClient(timeout=10.0, auth=(settings.imagekit_private_key, "")) as client:
                search = await client.get("https://api.imagekit.io/v1/files", params={"searchQuery": f'name="{file_id}"'})
                if search.status_code == 200 and search.json():
                    fid = search.json()[0]["fileId"]
                    await client.delete(f"https://api.imagekit.io/v1/files/{fid}")
            return

        if settings.github_storage_repo and "githubusercontent.com" in url:
            path = url.split(f"{settings.github_storage_repo}/")[-1].split("/", 1)[-1]
            async with httpx.AsyncClient(timeout=10.0) as client:
                get_resp = await client.get(
                    f"https://api.github.com/repos/{settings.github_storage_repo}/contents/{path}",
                    headers={"Authorization": f"Bearer {settings.github_storage_token}"},
                )
                if get_resp.status_code == 200:
                    sha = get_resp.json().get("sha")
                    await client.request(
                        "DELETE",
                        f"https://api.github.com/repos/{settings.github_storage_repo}/contents/{path}",
                        headers={"Authorization": f"Bearer {settings.github_storage_token}"},
                        json={"message": f"delete {path}", "sha": sha},
                    )
            return
    except Exception:
        logger.warning("delete_file_failed", extra={"extra_data": {"url": url}})