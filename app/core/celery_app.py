from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "mail_service",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    include=["app.tasks.mail_tasks"],
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    task_always_eager=settings.celery_task_always_eager,
    task_default_retry_delay=2,
)

celery_app.autodiscover_tasks(["app.tasks"])
