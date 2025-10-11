# Backend Installation & Structure Guide

## Installation

### 1. Requirements
- **Python** 3.11.9  
- **PostgreSQL** 16.10  
- **Docker** (optional, for database container)  
- **`be/` folder** (project root)

---

### 2. Virtual Environment Setup

```bash
python -m venv .venv

# Activate:
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Database Setup (via Docker)

```bash
docker run -d --name db \
  -e POSTGRES_PASSWORD=123456 \
  -p 5432:5432 \
  postgres:16
```

---

### 4. Run the Server

1. Copy `.env.example` to `.env` inside `be/app/`
2. Start the app:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Project Structure

```
be/
├── app/                    # Root application package
│   ├── db/                 # Database modules (connection, migrations, etc.)
│   ├── models/             # Pydantic & ORM models
│   ├── routers/            # API routes
│   ├── utils/              # Helper utilities (auth, logging, etc.)
│   ├── .env.example        # Example environment variables
│   ├── __init__.py         # Initialize something (e.g. job queue, db connection, etc.)
│   └── main.py             # Application entry point
│
├── test/                   # Unit tests (later uses)
└── requirements.txt        # Python dependencies
```
---

## Notes

- Make sure PostgreSQL service is running before starting the backend.  
- If using Docker, the default connection URL will be something like:  
  ```
  postgresql://postgres:123456@localhost:5432/postgres
  ```
- Add new dependencies via:
  ```bash
  pip install <package> && pip freeze > requirements.txt
  ```
