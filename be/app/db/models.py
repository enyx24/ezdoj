from app.db.connect_db import get_conn
import logging
from app.utils.auth import hash_password
import os

conn = get_conn()
cursor = conn.cursor()

#====USER TABLE====
cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'users'
        )
""")
if cursor.fetchone()[0] == False:
    # logging.info("Creatin users table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        full_name VARCHAR(100) NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    try:
        conn.commit()
        logging.info("Users table created successfully.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error creating users table: {e}")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "adminpass")
ADMIN_FULLNAME = os.getenv("ADMIN_FULLNAME", "Admin User")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")

cursor.execute("SELECT 1 FROM users WHERE username = %s", (ADMIN_USERNAME,))
if cursor.fetchone() is None:
    hashed_admin_password = hash_password(ADMIN_PASSWORD)
    cursor.execute(
        "INSERT INTO users (username, email, full_name, hashed_password) VALUES (%s, %s, %s, %s)",
        (ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_FULLNAME, hashed_admin_password)
    )
    try:
        conn.commit()
        logging.info("Admin user created successfully.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error creating admin user: {e}")



