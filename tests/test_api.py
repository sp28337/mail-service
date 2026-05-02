from unittest.mock import patch


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_send_mail_enqueues_task(client):
    payload = {"to": ["user@example.com"], "subject": "Hi", "text": "hello"}
    with patch("app.api.v1.mail.send_mail_task.delay") as mock_delay:
        mock_delay.return_value.id = "task-123"
        response = client.post("/v1/mail/send", json=payload)

    assert response.status_code == 202
    assert response.json()["task_id"] == "task-123"


def test_send_mail_validation(client):
    payload = {"to": ["user@example.com"], "subject": "Hi"}
    response = client.post("/v1/mail/send", json=payload)
    assert response.status_code == 422


def test_template_placeholder_validation(client):
    payload = {
        "to": ["user@example.com"],
        "subject": "Hi",
        "template_name": "string",
        "template_context": {"name": "User"},
    }
    response = client.post("/v1/mail/send", json=payload)
    assert response.status_code == 422
