import pytest

from app.schemas.mail import MailRequest
from app.services.mail_service import MailService


@pytest.mark.asyncio
async def test_mail_service_calls_provider(monkeypatch):
    captured = {}

    async def fake_send_raw(message: str, sender: str, recipients: list[str]) -> None:
        captured['message'] = message
        captured['sender'] = sender
        captured['recipients'] = recipients

    service = MailService()
    monkeypatch.setattr(service._provider, 'send_raw', fake_send_raw)

    req = MailRequest(to=['u@example.com'], subject='s', text='t')
    await service.send(req)

    assert 'Subject: s' in captured['message']
    assert captured['recipients'] == ['u@example.com']


def test_template_rendering():
    service = MailService()
    req = MailRequest(
        to=['u@example.com'],
        subject='templated',
        template_name='base_email.html',
        template_context={'title': 'Hello', 'body': 'World'},
    )
    msg = service._build_message(req)
    assert 'text/html' in msg.as_string()


def test_missing_template_falls_back_to_html():
    service = MailService()
    req = MailRequest(
        to=['u@example.com'],
        subject='templated',
        template_name='missing.html',
        html='<p>fallback</p>',
    )
    msg = service._build_message(req)
    assert 'fallback' in msg.as_string()


def test_missing_template_without_html_raises():
    service = MailService()
    req = MailRequest(
        to=['u@example.com'],
        subject='templated',
        template_name='missing.html',
    )
    with pytest.raises(ValueError):
        service._build_message(req)
