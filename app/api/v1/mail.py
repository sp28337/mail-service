from fastapi import APIRouter, HTTPException, status

from app.schemas.mail import MailEnqueueResponse, MailRequest
from app.tasks.mail_tasks import send_mail_task

router = APIRouter()


@router.post("/send", response_model=MailEnqueueResponse, status_code=status.HTTP_202_ACCEPTED)
async def send_mail(payload: MailRequest) -> MailEnqueueResponse:
    if not payload.text and not payload.html:
        raise HTTPException(status_code=422, detail="Either text or html is required")

    task = send_mail_task.delay(payload.model_dump(mode="json"))
    return MailEnqueueResponse(task_id=task.id, status="queued")
