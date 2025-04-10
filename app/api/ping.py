from fastapi import APIRouter, status

router = APIRouter(prefix="/ping", tags=["Ping"])

@router.get("/ping")
def ping():
    return {"status": "ok"}
