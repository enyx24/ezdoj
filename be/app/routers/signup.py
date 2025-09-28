from fastapi import APIRouter, Depends, HTTPException, Response
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.hash import bcrypt
from dotenv import load_dotenv
import hashlib
import os
from app.utils.auth import hash_password

from app.models.auth import SignupRequest, SignupResponse

router = APIRouter()

# ==== CONFIG ====
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 30))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# ==== MOCK DB ====
from app.utils.mock_db import fake_users_db

@router.post("/signup", response_model=SignupResponse)
async def signup(request: SignupRequest):
    if request.password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if request.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(request.password)
    fake_users_db[request.username] = {
        "username": request.username,
        "email": request.email,
        "full_name": request.full_name,
        "hashed_password": hashed_password,
    }

    return SignupResponse(message="User created successfully")