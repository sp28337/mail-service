from unittest.mock import AsyncMock, patch

from app.tasks.mail_tasks import send_mail_task


def test_send_mail_task_executes():
    payload = {"to": ["u@example.com"], "subject": "x", "text": "y"}
    with patch("app.tasks.mail_tasks.MailService.send", new_callable=AsyncMock) as mock_send:
        send_mail_task(payload)
    mock_send.assert_awaited_once()
