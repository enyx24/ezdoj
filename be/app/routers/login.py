from fastapi import APIRouter, Depends, HTTPException, Response
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.hash import bcrypt
from dotenv import load_dotenv
import hashlib
import os

from app.models.auth import LoginRequest

router = APIRouter()

# ==== CONFIG ====
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 30))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"


# ==== UTILS ====
def hash_password(password: str) -> str:
    """
    Hash password an toàn:
    - SHA256 trước để tránh giới hạn 72 bytes của bcrypt
    - bcrypt để lưu trong DB
    """
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.hash(digest)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    digest = hashlib.sha256(plain_password.encode("utf-8")).digest()
    return bcrypt.verify(digest, hashed_password)


def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ==== MOCK DB ====
fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": hash_password("secret123"),
    }
}

if DEBUG:
    print("DEBUG HASH:", hash_password("secret123"))

# ==== ROUTES ====
@router.post("/login")
async def login(request: LoginRequest, response: Response):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {"msg": "Login successful"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"msg": "Logged out"}
