from fastapi import APIRouter

from app.api.v1.mail import router as mail_router
from app.api.v1.system import router as system_router

router = APIRouter()
router.include_router(system_router)
router.include_router(mail_router, prefix="/v1/mail", tags=["mail"])
