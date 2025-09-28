import hashlib
from passlib.hash import bcrypt

def hash_password(password: str) -> str:
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.hash(digest)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    digest = hashlib.sha256(plain_password.encode("utf-8")).digest()
    return bcrypt.verify(digest, hashed_password)