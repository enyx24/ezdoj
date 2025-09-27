from fastapi import APIRouter

router = APIRouter()
@router.get("/users", tags=["users"], description="List users")
def get_users():
    return []