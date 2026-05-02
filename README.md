# Mail Service (FastAPI + Celery + Redis)

Production-ready starter for asynchronous email delivery.

## Features
- FastAPI REST API with OpenAPI docs.
- Async mail dispatch via Celery worker.
- Redis as broker/result backend.
- SMTP provider abstraction with template rendering (Jinja2).
- Retry with exponential backoff on transient failures.
- Strong request validation using Pydantic v2.
- Dockerized local environment.
- Test suite with API/service/task coverage.

## Architecture
See `docs/architecture.md`.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
uvicorn app.main:app --reload
```

In another terminal:
```bash
celery -A app.core.celery_app.celery_app worker --loglevel=INFO
```

## Docker
```bash
docker compose up --build
```

## API
- `GET /health`
- `GET /ready`
- `POST /v1/mail/send`

Example request:
```json
{
  "to": ["user@example.com"],
  "subject": "Welcome",
  "text": "Hello from mail service",
  "html": "<p>Hello from <b>mail service</b></p>",
  "metadata": {"tenant": "acme"}
}
```

## Testing
```bash
pytest
```

## Linting / Formatting
```bash
ruff check .
black --check .
```
