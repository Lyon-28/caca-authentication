import httpx
from app.config import settings

TEMPLATES = {
    "welcome": {
        "subject": "Selamat datang di {app_name}",
        "body": "<h2>Halo {name}</h2><p>Akun kamu berhasil dibuat di {app_name}.</p>",
    },
    "verify_email": {
        "subject": "Verifikasi email kamu",
        "body": "<h2>Verifikasi Email</h2><p>Klik link berikut untuk verifikasi email kamu:</p><p><a href=\"{link}\">Verifikasi Sekarang</a></p><p>Link berlaku 24 jam.</p>",
    },
    "reset_password": {
        "subject": "Reset password kamu",
        "body": "<h2>Reset Password</h2><p>Klik link berikut untuk reset password:</p><p><a href=\"{link}\">Reset Password</a></p><p>Link berlaku 1 jam. Abaikan jika bukan kamu.</p>",
    },
    "password_changed": {
        "subject": "Password kamu telah diubah",
        "body": "<h2>Password Diubah</h2><p>Password akun kamu baru saja diubah. Jika ini bukan kamu, segera amankan akun.</p>",
    },
    "new_device_login": {
        "subject": "Login dari perangkat baru",
        "body": "<h2>Login Baru Terdeteksi</h2><p>Perangkat: {device}</p><p>Lokasi: {location}</p><p>Waktu: {time}</p><p>Jika ini bukan kamu, segera ubah password.</p>",
    },
    "suspicious_activity": {
        "subject": "Aktivitas mencurigakan terdeteksi",
        "body": "<h2>Aktivitas Mencurigakan</h2><p>{detail}</p><p>Jika ini bukan kamu, segera amankan akun kamu.</p>",
    },
    "magic_link": {
        "subject": "Link login kamu",
        "body": "<h2>Login Tanpa Password</h2><p><a href=\"{link}\">Klik di sini untuk login</a></p><p>Link berlaku 15 menit.</p>",
    },
    "newsletter": {
        "subject": "{subject}",
        "body": "{body}",
    },
}

def render_template(name: str, context: dict) -> tuple[str, str]:
    tpl = TEMPLATES[name]
    subject = tpl["subject"].format(**context)
    body = tpl["body"].format(**context)
    return subject, body

async def _try_resend(to: str, subject: str, body: str) -> bool:
    if not settings.resend_api_key:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {settings.resend_api_key}"},
                json={"from": "noreply@caca-auth.dev", "to": [to], "subject": subject, "html": body},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_brevo(to: str, subject: str, body: str) -> bool:
    if not settings.brevo_api_key:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                "https://api.brevo.com/v3/smtp/email",
                headers={"api-key": settings.brevo_api_key},
                json={"sender": {"email": "noreply@caca-auth.dev"}, "to": [{"email": to}], "subject": subject, "htmlContent": body},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_mailjet(to: str, subject: str, body: str) -> bool:
    if not settings.mailjet_api_key:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0, auth=(settings.mailjet_api_key, settings.mailjet_secret_key)) as client:
            resp = await client.post(
                "https://api.mailjet.com/v3.1/send",
                json={"Messages": [{"From": {"Email": "noreply@caca-auth.dev"}, "To": [{"Email": to}], "Subject": subject, "HTMLPart": body}]},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_smtp_gmail(to: str, subject: str, body: str) -> bool:
    if not settings.smtp_gmail_user:
        return False
    try:
        import aiosmtplib
        from email.mime.text import MIMEText
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = settings.smtp_gmail_user
        msg["To"] = to
        await aiosmtplib.send(
            msg, hostname="smtp.gmail.com", port=587, start_tls=True,
            username=settings.smtp_gmail_user, password=settings.smtp_gmail_pass,
        )
        return True
    except Exception:
        return False

async def _try_mailgun(to: str, subject: str, body: str) -> bool:
    if not settings.mailgun_api_key:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0, auth=("api", settings.mailgun_api_key)) as client:
            resp = await client.post(
                f"https://api.mailgun.net/v3/{settings.mailgun_domain}/messages",
                data={"from": f"noreply@{settings.mailgun_domain}", "to": to, "subject": subject, "html": body},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_sendgrid(to: str, subject: str, body: str) -> bool:
    if not settings.sendgrid_api_key:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={"Authorization": f"Bearer {settings.sendgrid_api_key}"},
                json={"personalizations": [{"to": [{"email": to}]}], "from": {"email": "noreply@caca-auth.dev"}, "subject": subject, "content": [{"type": "text/html", "value": body}]},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_firebase(to: str, subject: str, body: str) -> bool:
    return False

async def _try_supabase(to: str, subject: str, body: str) -> bool:
    return False

async def _try_ntfy(to: str, subject: str, body: str) -> bool:
    if not settings.ntfy_url:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(settings.ntfy_url, content=f"{subject}\nUntuk: {to}\n{body[:200]}".encode())
            return resp.status_code < 300
    except Exception:
        return False

async def _try_gotify(to: str, subject: str, body: str) -> bool:
    if not settings.gotify_url:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{settings.gotify_url}/message?token={settings.gotify_token}",
                json={"title": subject, "message": f"Untuk: {to}\n{body[:200]}"},
            )
            return resp.status_code < 300
    except Exception:
        return False

async def _try_apprise(to: str, subject: str, body: str) -> bool:
    if not settings.apprise_url:
        return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(settings.apprise_url, json={"title": subject, "body": f"Untuk: {to}\n{body[:200]}"})
            return resp.status_code < 300
    except Exception:
        return False

EMAIL_CHAIN = [
    _try_resend, _try_brevo, _try_mailjet, _try_smtp_gmail, _try_mailgun,
    _try_sendgrid, _try_firebase, _try_supabase, _try_ntfy, _try_gotify, _try_apprise,
]

async def send_email(to: str, template_name: str, context: dict) -> dict:
    subject, body = render_template(template_name, context)
    for provider_fn in EMAIL_CHAIN:
        sent = await provider_fn(to, subject, body)
        if sent:
            return {"sent": True, "provider": provider_fn.__name__.replace("_try_", "")}
    return {"sent": False, "provider": "ui_alert_fallback", "subject": subject, "body": body}