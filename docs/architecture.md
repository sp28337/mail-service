# Architecture

## Components
1. **FastAPI API**
   - Validates input and enqueues Celery tasks.
2. **Celery Worker**
   - Executes email sending with retries/backoff.
3. **Redis**
   - Celery broker and result backend.
4. **Mail Service Layer**
   - Builds MIME messages and renders Jinja templates.
5. **SMTP Provider**
   - Concrete provider implementation; can be swapped for SES/SendGrid providers.

## Flow
1. Client calls `POST /v1/mail/send`.
2. API validates payload and queues `send_mail_task`.
3. Worker consumes task, constructs and sends MIME email.
4. Retries happen automatically on transient exceptions.
