from unittest.mock import patch


def test_send_sample_order_enqueues_task(client):
    payload = {
        "name": "Иван Иванов",
        "phone": "+79001234567",
        "articles": "ART-001, ART-002",
        "wood_sort": "Дуб",
    }
    with patch("app.api.v1.notify.send_mail_task.delay") as mock_delay:
        mock_delay.return_value.id = "task-sample-1"
        response = client.post("/notify-mail/send-sample-order", json=payload)

    assert response.status_code == 202
    assert response.json()["task_id"] == "task-sample-1"
    assert response.json()["status"] == "queued"
    mock_delay.assert_called_once()
    enqueued = mock_delay.call_args[0][0]
    assert enqueued["template_name"] == "sample_order_email.html"
    assert enqueued["template_context"]["name"] == "Иван Иванов"
    assert enqueued["template_context"]["wood_sort"] == "Дуб"


def test_send_calc_order_enqueues_task(client):
    payload = {
        "name": "Мария Петрова",
        "phone": "+79009876543",
        "area": "45 кв.м",
        "article": "ART-100",
    }
    with patch("app.api.v1.notify.send_mail_task.delay") as mock_delay:
        mock_delay.return_value.id = "task-calc-1"
        response = client.post("/notify-mail/send-calc-order", json=payload)

    assert response.status_code == 202
    assert response.json()["task_id"] == "task-calc-1"
    mock_delay.assert_called_once()
    enqueued = mock_delay.call_args[0][0]
    assert enqueued["template_name"] == "calc_order_email.html"
    assert enqueued["template_context"]["area"] == "45 кв.м"
    assert enqueued["template_context"]["article"] == "ART-100"


def test_send_calc_order_without_article(client):
    payload = {
        "name": "Алексей",
        "phone": "+79001111111",
        "area": "20 кв.м",
    }
    with patch("app.api.v1.notify.send_mail_task.delay") as mock_delay:
        mock_delay.return_value.id = "task-calc-2"
        response = client.post("/notify-mail/send-calc-order", json=payload)

    assert response.status_code == 202
    enqueued = mock_delay.call_args[0][0]
    assert "article" not in enqueued["template_context"]


def test_send_sample_order_missing_field(client):
    payload = {"name": "Test", "phone": "+79001234567", "articles": "ART-001"}
    response = client.post("/notify-mail/send-sample-order", json=payload)
    assert response.status_code == 422


def test_send_calc_order_missing_field(client):
    payload = {"name": "Test", "phone": "+79001234567"}
    response = client.post("/notify-mail/send-calc-order", json=payload)
    assert response.status_code == 422
