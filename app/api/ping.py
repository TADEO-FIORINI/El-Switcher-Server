from fastapi import APIRouter, status

router = APIRouter(prefix="/ping", tags=["Ping"])

@router.get("")
def ping():
    return {"status": "ok"}
