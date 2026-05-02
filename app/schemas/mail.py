from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class MailRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    to: list[EmailStr] = Field(min_length=1)
    subject: str = Field(min_length=1, max_length=255)
    text: str | None = Field(default=None, max_length=100000)
    html: str | None = Field(default=None, max_length=100000)
    cc: list[EmailStr] = Field(default_factory=list)
    bcc: list[EmailStr] = Field(default_factory=list)
    reply_to: EmailStr | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    template_name: str | None = None
    template_context: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_body_presence(self) -> "MailRequest":
        if not self.text and not self.html and not self.template_name:
            raise ValueError("One of text, html, or template_name is required")
        return self


class MailEnqueueResponse(BaseModel):
    task_id: str
    status: str
