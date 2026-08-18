import pyotp
import qrcode
import io
import base64

def generate_totp_secret() -> str:
    return pyotp.random_base32()

def get_provisioning_uri(secret: str, email: str, issuer: str = "Caca Auth") -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name=issuer)

def generate_qr_base64(uri: str) -> str:
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def verify_totp_code(secret: str, code: str) -> bool:
    return pyotp.TOTP(secret).verify(code, valid_window=1)