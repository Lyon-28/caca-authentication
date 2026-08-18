import httpx
from app.config import settings

async def _try_zenziva(to: str, message: str) -> bool:
    if not settings.zenziva_api_key:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                "https://console.zenziva.net/wareguler/api/sendWA/",
                data={"userkey": settings.zenziva_user_key, "passkey": settings.zenziva_api_key, "to": to, "message": message},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_twilio(to: str, message: str) -> bool:
    if not settings.twilio_sid:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0, auth=(settings.twilio_sid, settings.twilio_token)) as client:
            resp = await client.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{settings.twilio_sid}/Messages.json",
                data={"From": settings.twilio_from, "To": to, "Body": message},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_vonage(to: str, message: str) -> bool:
    if not settings.vonage_api_key:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                "https://rest.nexmo.com/sms/json",
                data={"api_key": settings.vonage_api_key, "api_secret": settings.vonage_api_secret, "to": to, "from": "CacaAuth", "text": message},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_termii(to: str, message: str) -> bool:
    if not settings.termii_api_key:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                "https://api.ng.termii.com/api/sms/send",
                json={"api_key": settings.termii_api_key, "to": to, "from": "CacaAuth", "sms": message, "type": "plain", "channel": "generic"},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_fonnte(to: str, message: str) -> bool:
    if not settings.fonnte_token:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                "https://api.fonnte.com/send",
                headers={"Authorization": settings.fonnte_token},
                data={"target": to, "message": message},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_wablas(to: str, message: str) -> bool:
    if not settings.wablas_token:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                "https://console.wablas.com/api/send-message",
                headers={"Authorization": settings.wablas_token},
                data={"phone": to, "message": message},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_messagebird(to: str, message: str) -> bool:
    if not settings.messagebird_api_key:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                "https://rest.messagebird.com/messages",
                headers={"Authorization": f"AccessKey {settings.messagebird_api_key}"},
                data={"originator": "CacaAuth", "recipients": to, "body": message},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_firebase(to: str, message: str) -> bool:
    return False

async def _try_supabase(to: str, message: str) -> bool:
    return False

async def _try_telegram(to: str, message: str) -> bool:
    if not settings.telegram_bot_token:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage",
                json={"chat_id": to, "text": message},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_meta_whatsapp(to: str, message: str) -> bool:
    if not settings.meta_wa_token:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"https://graph.facebook.com/v19.0/{settings.meta_wa_phone_id}/messages",
                headers={"Authorization": f"Bearer {settings.meta_wa_token}"},
                json={"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": message}},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_ntfy(to: str, message: str) -> bool:
    if not settings.ntfy_url:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(settings.ntfy_url, content=f"SMS untuk {to}: {message}".encode())
            return resp.status_code < 300
    except Exception:
        return False

async def _try_gotify(to: str, message: str) -> bool:
    if not settings.gotify_url:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{settings.gotify_url}/message?token={settings.gotify_token}",
                json={"title": "SMS/OTP", "message": f"Untuk {to}: {message}"},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_apprise(to: str, message: str) -> bool:
    if not settings.apprise_url:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(settings.apprise_url, json={"title": "SMS/OTP", "body": f"Untuk {to}: {message}"})
            return resp.status_code < 300
    except Exception:
        return False

async def _try_textbee(to: str, message: str) -> bool:
    if not settings.textbee_api_key:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                "https://api.textbee.dev/api/v1/gateway/devices/send-sms",
                headers={"x-api-key": settings.textbee_api_key},
                json={"recipients": [to], "message": message},
            )
            return resp.status_code < 300
    except Exception:
        return False

SMS_CHAIN = [
    _try_zenziva, _try_twilio, _try_vonage, _try_termii, _try_fonnte, _try_wablas,
    _try_messagebird, _try_firebase, _try_supabase, _try_telegram, _try_meta_whatsapp,
    _try_ntfy, _try_gotify, _try_apprise, _try_textbee,
]

async def send_sms(to: str, message: str) -> dict:
    for provider_fn in SMS_CHAIN:
        sent = await provider_fn(to, message)
        if sent:
            return {"sent": True, "provider": provider_fn.__name__.replace("_try_", "")}
    return {"sent": False, "provider": "ui_alert_fallback", "message": message}