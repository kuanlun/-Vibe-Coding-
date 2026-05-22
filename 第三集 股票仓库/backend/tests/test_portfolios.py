import pytest


def test_create_portfolio(client, auth_headers):
    response = client.post(
        "/api/portfolios",
        json={
            "market": "A股",
            "symbol": "600000",
            "name": "浦发银行",
            "shares": 100,
            "cost_price": 10.5,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["market"] == "A股"
    assert data["symbol"] == "600000"
    assert data["shares"] == 100.0


def test_get_portfolios(client, auth_headers):
    client.post(
        "/api/portfolios",
        json={
            "market": "美股",
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "shares": 50,
            "cost_price": 150.0,
        },
        headers=auth_headers,
    )
    response = client.get("/api/portfolios", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_update_portfolio(client, auth_headers):
    create_response = client.post(
        "/api/portfolios",
        json={
            "market": "台股",
            "symbol": "2330",
            "name": "台积电",
            "shares": 10,
            "cost_price": 500.0,
        },
        headers=auth_headers,
    )
    portfolio_id = create_response.json()["id"]
    response = client.put(
        f"/api/portfolios/{portfolio_id}",
        json={"shares": 20},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["shares"] == 20.0


def test_delete_portfolio(client, auth_headers):
    create_response = client.post(
        "/api/portfolios",
        json={
            "market": "A股",
            "symbol": "000001",
            "name": "平安银行",
            "shares": 200,
            "cost_price": 12.0,
        },
        headers=auth_headers,
    )
    portfolio_id = create_response.json()["id"]
    response = client.delete(f"/api/portfolios/{portfolio_id}", headers=auth_headers)
    assert response.status_code == 200