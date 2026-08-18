# Caca Auth

Auth-as-a-Service 

## Setup
1. `cp .env.example .env` lalu isi kredensial (Neon, Upstash, provider email/SMS/OAuth sesuai kebutuhan — semua opsional, sistem tetap jalan dengan fallback UI alert jika kosong)
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload`

## Dashboard
- Admin: `/static/admin/index.html`
- Dokumentasi: `/static/docs/index.html`
- Swagger: `/docs`

## Catatan Produksi
- `admin_routes.py`: ganti token placeholder dengan JWT admin bertanda tangan sebelum production.
- Apple OAuth butuh JWT client_secret dari private key `.p8`, generate terpisah.
- Deploy: Railway/Render/Fly.io direkomendasikan; Vercel serverless kurang ideal untuk pool DB async.

## Instagram Login — keterbatasan penting
Instagram Basic Display API sudah di-deprecate Meta per Desember 2024 dan tidak berfungsi lagi.
Satu-satunya jalur OAuth Instagram yang aktif sekarang ("Instagram API with Instagram Login")
HANYA menerima akun Instagram Business/Creator — akun personal biasa TIDAK BISA login lewat jalur ini.
Jika target end-user aplikasi kamu adalah pengguna Instagram personal, "Login with Instagram"
secara teknis tidak tersedia di ekosistem Meta saat ini. Endpoint ini disediakan untuk kasus
di mana user diharapkan adalah pemilik akun bisnis/creator saja.

## Testing
`pytest tests/ -v`