import pytest


def test_create_alert(client, auth_headers):
    response = client.post(
        "/api/alerts",
        json={
            "symbol": "AAPL",
            "condition": "高于",
            "target_price": 200.0,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["condition"] == "高于"
    assert data["target_price"] == 200.0


def test_get_alerts(client, auth_headers):
    client.post(
        "/api/alerts",
        json={
            "symbol": "TSLA",
            "condition": "低于",
            "target_price": 700.0,
        },
        headers=auth_headers,
    )
    response = client.get("/api/alerts", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_delete_alert(client, auth_headers):
    create_response = client.post(
        "/api/alerts",
        json={
            "symbol": "MSFT",
            "condition": "高于",
            "target_price": 400.0,
        },
        headers=auth_headers,
    )
    alert_id = create_response.json()["id"]
    response = client.delete(f"/api/alerts/{alert_id}", headers=auth_headers)
    assert response.status_code == 200