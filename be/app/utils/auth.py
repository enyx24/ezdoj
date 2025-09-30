import hashlib
from passlib.hash import bcrypt
from app.db.connect_db import get_conn
import logging
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.hash import bcrypt
import os

conn = get_conn()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 30))

def hash_password(password: str) -> str:
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.hash(digest)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    digest = hashlib.sha256(plain_password.encode("utf-8")).digest()
    return bcrypt.verify(digest, hashed_password)

def authenticate_user(username: str, password: str):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username, hashed_password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            user = {"username": user[0], "hashed_password": user[1]}
    except Exception as e:
        logging.error(f"Error authenticating user: {e}")
        user = None
    finally:
        cursor.close()
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def check_user_exists(username: str) -> bool:
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        exists = cursor.fetchone() is not None
    except Exception as e:
        logging.error(f"Error checking if user exists: {e}")
        exists = False
    finally:
        cursor.close()
    return exists

def create_user(username: str, email: str, full_name: str, hashedpassword: str) -> None:
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, full_name, hashed_password) VALUES (%s, %s, %s, %s)",
            (username, email, full_name, hashedpassword)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Error creating user: {e}")
    finally:
        cursor.close()
    return

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str):
    if not token:
        return None
    try:
        credentials = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except Exception as e:
        logging.error(f"Error occurred while decoding token: {e}")
        return None
    username: str = credentials.get("sub")
    return username