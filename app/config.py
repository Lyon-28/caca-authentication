from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    env: str = "development"
    
    frontend_url: str = "http://localhost:3000"

    resend_api_key: str = ""
    brevo_api_key: str = ""
    mailjet_api_key: str = ""
    mailjet_secret_key: str = ""
    smtp_gmail_user: str = ""
    smtp_gmail_pass: str = ""
    mailgun_api_key: str = ""
    mailgun_domain: str = ""
    sendgrid_api_key: str = ""
    firebase_api_key: str = ""
    supabase_url: str = ""
    supabase_service_key: str = ""
    ntfy_url: str = ""
    gotify_url: str = ""
    gotify_token: str = ""
    apprise_url: str = ""

    zenziva_api_key: str = ""
    zenziva_user_key: str = ""
    twilio_sid: str = ""
    twilio_token: str = ""
    twilio_from: str = ""
    vonage_api_key: str = ""
    vonage_api_secret: str = ""
    termii_api_key: str = ""
    fonnte_token: str = ""
    wablas_token: str = ""
    messagebird_api_key: str = ""
    telegram_bot_token: str = ""
    meta_wa_token: str = ""
    meta_wa_phone_id: str = ""
    textbee_api_key: str = ""

    ipapi_url: str = "https://ipapi.co"
    ipgeolocation_api_key: str = ""

    google_client_id: str = ""
    google_client_secret: str = ""
    github_client_id: str = ""
    github_client_secret: str = ""
    apple_client_id: str = ""
    apple_team_id: str = ""
    apple_key_id: str = ""
    apple_private_key_path: str = "./secrets/apple_auth_key.p8"
    facebook_client_id: str = ""
    facebook_client_secret: str = ""
    microsoft_client_id: str = ""
    microsoft_client_secret: str = ""
    twitter_client_id: str = ""
    twitter_client_secret: str = ""
    linkedin_client_id: str = ""
    linkedin_client_secret: str = ""
    discord_client_id: str = ""
    discord_client_secret: str = ""
    instagram_app_id: str = ""
    instagram_app_secret: str = ""
    oauth_redirect_base: str = "http://localhost:8000"

    supabase_storage_bucket: str = "avatars"
    imagekit_private_key: str = ""
    imagekit_public_key: str = ""
    imagekit_url_endpoint: str = ""
    imgbb_api_key: str = ""
    github_storage_token: str = ""
    github_storage_repo: str = ""
    local_storage_path: str = "./static/uploads"

    datadog_api_key: str = ""
    axiom_api_token: str = ""
    axiom_dataset: str = ""
    betterstack_source_token: str = ""
    log_level: str = "INFO"
    admin_email: str = ""
    admin_password_hash: str = ""
    
    class Config:
        env_file = ".env"
settings = Settings()