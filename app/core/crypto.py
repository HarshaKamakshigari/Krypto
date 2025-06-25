import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

FERNET_KEY = os.getenv("FERNET_KEY")

if not FERNET_KEY:
    raise ValueError("FERNET_KEY is missing from .env.local")

cipher = Fernet(FERNET_KEY.encode())

def encrypt_secret(secret: str) -> str:
    return cipher.encrypt(secret.encode()).decode()

def decrypt_secret(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()
