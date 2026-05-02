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
- CI pipeline with linting + tests on GitHub Actions.

## Architecture
See `docs/architecture.md`.

## Quickstart (uv)
```bash
uv venv
source .venv/bin/activate
uv sync --extra dev
cp .env.example .env
uv run uvicorn app.main:app --reload
```

In another terminal:
```bash
uv run celery -A app.core.celery_app.celery_app worker --loglevel=INFO
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
uv run pytest
```

## Linting / Formatting
```bash
uv run ruff check .
uv run black --check .
```
