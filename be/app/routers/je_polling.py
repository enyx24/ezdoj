from fastapi import APIRouter, Depends, HTTPException
from app.models.je_auth import PollingRequest
from app.utils.auth import authenticate_user
from app import active_judges
import time

router = APIRouter()

@router.post("/je/polling")
async def je_auth(request: JEPollingRequest):
    je_id = request.je_id
    status = request.status
    current_task = request.current_task
    ping = request.ping

    if je_id not in active_judges:
        raise HTTPException(status_code=401, detail="Invalid JE ID")

    active_judges[je_id]["last_heartbeat"] = time.time()
    active_judges[je_id]["status"] = status
    active_judges[je_id]["current_task"] = current_task
    active_judges[je_id]["ping"] = ping

    job = get_job()

    return {"status": "success", "job": job}