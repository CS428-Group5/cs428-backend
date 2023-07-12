from datetime import datetime, timedelta
from jwt import encode, decode, InvalidTokenError, ExpiredSignatureError
import os

# This is to get the secret key from the environment
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
TOKEN_EXPIRATION = int(os.getenv("TOKEN_EXPIRATION", "5"))

def create_token(user_id: int, username: str) -> str:
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION)
    }
    token = encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token: str):
    try:
        payload = decode(token, SECRET_KEY, algorithms='HS256')
        return payload["user_id"], payload["username"]
    except (InvalidTokenError, ExpiredSignatureError):
        return None
