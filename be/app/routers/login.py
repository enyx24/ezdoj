from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

from models.auth import LoginRequest

router = APIRouter()

# Load env variables
load_dotenv()
# ==== CONFIG ====
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Giả sử DB (mock)
fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash("secret123"),
    }
}

# ==== UTILS ====
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

    # Set cookie ttl
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
