from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.schemas.mail import MailEnqueueResponse, MailRequest
from app.schemas.notify import OrderCalculationSchema, OrderSampleSchema
from app.tasks.mail_tasks import send_mail_task

router = APIRouter()


def _get_notification_recipient() -> str:
    """Return the configured notification recipient or raise 503 if not set."""
    settings = get_settings()
    recipient = settings.default_reply_to
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Notification recipient (MAIL_REPLY_TO) is not configured.",
        )
    return recipient


@router.post(
    "/send-sample-order",
    response_model=MailEnqueueResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def send_sample_order(payload: OrderSampleSchema) -> MailEnqueueResponse:
    recipient = _get_notification_recipient()
    mail_request = MailRequest(
        to=[recipient],
        subject="Новая заявка на образцы",
        template_name="sample_order_email.html",
        template_context={
            "name": payload.name,
            "phone": payload.phone,
            "articles": payload.articles,
            "wood_sort": payload.wood_sort,
        },
    )
    task = send_mail_task.delay(mail_request.model_dump(mode="json"))
    return MailEnqueueResponse(task_id=task.id, status="queued")


@router.post(
    "/send-calc-order",
    response_model=MailEnqueueResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def send_calc_order(payload: OrderCalculationSchema) -> MailEnqueueResponse:
    recipient = _get_notification_recipient()
    template_context: dict[str, str] = {
        "name": payload.name,
        "phone": payload.phone,
        "area": payload.area,
    }
    if payload.article is not None:
        template_context["article"] = payload.article

    mail_request = MailRequest(
        to=[recipient],
        subject="Новая заявка на расчёт",
        template_name="calc_order_email.html",
        template_context=template_context,
    )
    task = send_mail_task.delay(mail_request.model_dump(mode="json"))
    return MailEnqueueResponse(task_id=task.id, status="queued")
