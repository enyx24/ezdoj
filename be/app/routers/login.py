from fastapi import APIRouter, Depends, HTTPException, Response
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.hash import bcrypt
from dotenv import load_dotenv
import hashlib
import os
from app.utils.auth import authenticate_user
from app.models.auth import LoginRequest
from app.utils.mock_db import fake_users_db

router = APIRouter()

# ==== CONFIG ====
# load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 30))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


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
