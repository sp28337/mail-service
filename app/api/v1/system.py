from celery.exceptions import CeleryError
from fastapi import APIRouter, HTTPException

from app.core.celery_app import celery_app
from app.core.config import get_settings

router = APIRouter()


@router.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def readiness() -> dict[str, str]:
    settings = get_settings()
    if not settings.redis_url:
        raise HTTPException(status_code=503, detail="redis_url is not configured")

    try:
        celery_app.control.ping(timeout=1.0)
    except CeleryError as exc:
        raise HTTPException(status_code=503, detail="celery is unavailable") from exc

    return {"status": "ready"}
