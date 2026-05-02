from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = Field(default="dev", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    celery_broker_url: str = Field(default="redis://redis:6379/0", alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://redis:6379/1", alias="CELERY_RESULT_BACKEND")
    celery_task_always_eager: bool = Field(default=False, alias="CELERY_TASK_ALWAYS_EAGER")

    smtp_host: str = Field(default="localhost", alias="SMTP_HOST")
    smtp_port: int = Field(default=1025, alias="SMTP_PORT")
    smtp_username: str | None = Field(default=None, alias="SMTP_USERNAME")
    smtp_password: str | None = Field(default=None, alias="SMTP_PASSWORD")
    smtp_use_tls: bool = Field(default=False, alias="SMTP_USE_TLS")
    smtp_use_starttls: bool = Field(default=False, alias="SMTP_USE_STARTTLS")
    default_from_name: str = Field(default="Mail Service", alias="MAIL_FROM_NAME")
    default_from_email: str = Field(default="no-reply@example.com", alias="MAIL_FROM_EMAIL")
    default_reply_to: str | None = Field(default=None, alias="MAIL_REPLY_TO")

    template_directory: str = Field(default="app/templates", alias="TEMPLATE_DIRECTORY")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
