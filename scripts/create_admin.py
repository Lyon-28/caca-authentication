import sys
sys.path.append(".")
from app.security import hash_password

password = input("Password admin: ")
print("\nADMIN_PASSWORD_HASH=" + hash_password(password))
print("Salin baris di atas ke file .env kamu (bersama ADMIN_EMAIL).")