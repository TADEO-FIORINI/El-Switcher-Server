from fastapi import APIRouter, status

router = APIRouter(prefix="/ping", tags=["Ping"])

@router.api_route("", methods=["GET", "HEAD"])
def ping():
    return {"status": "ok"}