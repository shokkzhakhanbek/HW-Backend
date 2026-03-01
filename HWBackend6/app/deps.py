import hashlib
import hmac
import base64
import json
import time
from fastapi import Request, HTTPException
from app.settings import SECRET_KEY, JWT_COOKIE_NAME


def hash_password(password: str) -> str:
    salt = "static_salt"
    return hashlib.sha256((salt + password).encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)


def create_jwt(payload: dict) -> str:
    payload["exp"] = int(time.time()) + 60 * 60 * 24  # 1 день
    data = json.dumps(payload).encode()
    b64 = base64.urlsafe_b64encode(data).decode()
    signature = hmac.new(SECRET_KEY.encode(), b64.encode(), hashlib.sha256).hexdigest()
    return f"{b64}.{signature}"


def decode_jwt(token: str) -> dict:
    try:
        b64, signature = token.split(".")
        expected_signature = hmac.new(
            SECRET_KEY.encode(), b64.encode(), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            raise Exception("Invalid signature")

        payload = json.loads(base64.urlsafe_b64decode(b64.encode()))

        if payload["exp"] < int(time.time()):
            raise Exception("Token expired")

        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(request: Request):
    token = request.cookies.get(JWT_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401)

    payload = decode_jwt(token)
    user_id = payload["user_id"]

    user = request.app.state.users_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401)

    return user