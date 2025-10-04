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

#====PROBLEMS TABLE====
cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'problems'
        )
""")
if cursor.fetchone()[0] == False:
    # logging.info("Creating problems table...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id SERIAL PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        description TEXT NOT NULL,
        pdf_dir VARCHAR(255),
        sample_input TEXT,
        sample_output TEXT,
        time_limit INT NOT NULL,
        memory_limit INT NOT NULL,
        language_restrictions VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    try:
        conn.commit()
        logging.info("Problems table created successfully.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error creating problems table: {e}")

cursor.execute("""
    SELECT 1 FROM problems WHERE id = 1
""")
if cursor.fetchone() is None:
    cursor.execute("""
        INSERT INTO problems (title, description, pdf_dir, sample_input, sample_output, time_limit, memory_limit)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        "A + B",
        "Read two integers and output their sum.",
        "",
        "1 2\n",
        "3\n",
        1,
        256
    ))
    try:
        conn.commit()
        logging.info("Sample problem inserted successfully.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting sample problem: {e}")

#====SUBMISSIONS TABLE====
cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'submissions'
        )
""")
if cursor.fetchone()[0] == False:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions(
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id) ON DELETE CASCADE,
                problem_id INT REFERENCES problems(id) ON DELETE CASCADE,
                code TEXT NOT NULL,
                language_id INT NOT NULL,
                status VARCHAR(50) NOT NULL,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
""")
    try:
        conn.commit()
        logging.info("Submissions table created successfully.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error creating submissions table: {e}")



