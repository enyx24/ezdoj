from fastapi import APIRouter, HTTPException
import os
from app.utils.auth import *
from app.models.auth import SignupRequest, SignupResponse

router = APIRouter()

# ==== CONFIG ====
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 30))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# ==== MOCK DB ====

@router.post("/signup", response_model=SignupResponse)
async def signup(request: SignupRequest):
    
    if request.password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if check_user_exists(request.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(request.password)
    create_user(
        username=request.username,
        email=request.email,
        full_name=request.full_name,
        hashedpassword=hashed_password
    )

    return SignupResponse(message="User created successfully")