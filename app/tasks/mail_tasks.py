import logging

from celery import Task
from celery.exceptions import MaxRetriesExceededError

from app.core.celery_app import celery_app
from app.schemas.mail import MailRequest
from app.services.mail_service import MailService

logger = logging.getLogger(__name__)


@celery_app.task(
    name="app.tasks.mail_tasks.send_mail_task",
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=5,
)
def send_mail_task(self: Task, payload: dict) -> None:
    request = MailRequest(**payload)
    service = MailService()
    try:
        import asyncio

        asyncio.run(service.send(request))
        logger.info(
            "mail_dispatched",
            extra={"to": [str(e) for e in request.to], "subject": request.subject},
        )
    except MaxRetriesExceededError:
        logger.exception("mail_retry_exhausted")
        raise
