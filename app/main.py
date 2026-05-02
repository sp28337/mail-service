from fastapi import FastAPI

from app.api.routes import router
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="Mail Service", version="1.0.0")
app.include_router(router)
