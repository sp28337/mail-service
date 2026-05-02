from dataclasses import dataclass

import aiosmtplib


@dataclass(frozen=True)
class SMTPConfig:
    host: str
    port: int
    username: str | None
    password: str | None
    use_tls: bool
    use_starttls: bool


class SMTPProvider:
    def __init__(self, config: SMTPConfig) -> None:
        self._config = config

    async def send_raw(self, message: str, sender: str, recipients: list[str]) -> None:
        await aiosmtplib.send(
            message,
            hostname=self._config.host,
            port=self._config.port,
            username=self._config.username,
            password=self._config.password,
            use_tls=self._config.use_tls,
            start_tls=self._config.use_starttls,
            sender=sender,
            recipients=recipients,
        )
