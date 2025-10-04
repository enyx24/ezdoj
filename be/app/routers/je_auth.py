from fastapi import APIRouter, Depends, HTTPException
from app.models.je_auth import JEAuthRequest, JEAuthResponse
from app.utils.auth import authenticate_user
from app import active_judges
import time

router = APIRouter()

@router.post("/je/auth")
async def je_auth(request: JEAuthRequest):
    username = request.user
    password = request.password
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        active_judges[username] = {
            "last_heartbeat": time.time(),
            "status": "ready",
            "current_task": None,
            "ping": None
            }
        return JEAuthResponse(status="success", je_id=user["username"])