from app.utils.auth import hash_password
# ==== MOCK DB ====
fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": hash_password("secret123"),
    }
}