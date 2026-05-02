from email.message import EmailMessage

from app.core.config import get_settings
from app.schemas.mail import MailRequest
from app.services.providers import SMTPConfig, SMTPProvider
from app.services.templates import TemplateRenderer


class MailService:
    def __init__(self) -> None:
        settings = get_settings()
        self._settings = settings
        self._provider = SMTPProvider(
            SMTPConfig(
                host=settings.smtp_host,
                port=settings.smtp_port,
                username=settings.smtp_username,
                password=settings.smtp_password,
                use_tls=settings.smtp_use_tls,
                use_starttls=settings.smtp_use_starttls,
            )
        )
        self._renderer = TemplateRenderer(settings.template_directory)

    async def send(self, request: MailRequest) -> None:
        message = self._build_message(request)
        recipients = [*request.to, *request.cc, *request.bcc]
        await self._provider.send_raw(
            message=message.as_string(),
            sender=message["From"],
            recipients=[str(r) for r in recipients],
        )

    def _build_message(self, request: MailRequest) -> EmailMessage:
        message = EmailMessage()
        from_field = f"{self._settings.default_from_name} <{self._settings.default_from_email}>"
        message["From"] = from_field
        message["To"] = ", ".join([str(email) for email in request.to])
        if request.cc:
            message["Cc"] = ", ".join([str(email) for email in request.cc])
        message["Subject"] = request.subject
        if request.reply_to or self._settings.default_reply_to:
            message["Reply-To"] = str(request.reply_to or self._settings.default_reply_to)

        text_body = request.text or ""
        html_body = request.html
        if request.template_name:
            html_body = self._renderer.render(request.template_name, request.template_context)

        message.set_content(text_body or "This message contains HTML content.")
        if html_body:
            message.add_alternative(html_body, subtype="html")
        return message
