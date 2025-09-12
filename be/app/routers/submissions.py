from fastapi import APIRouter

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("/")
def create_submission():
    return {"id": 1, "status": "queued"}
