from fastapi import FastAPI
from app.routers import health, users, submissions, login

app = FastAPI(title="ezdoj", version="0.1.0")

# @app.get("/health")
# def health_check():
#     return {"status": "ok"}

app.include_router(health.router)
app.include_router(users.router)
app.include_router(submissions.router)
app.include_router(login.router)