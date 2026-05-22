import pytest


def test_export_csv(client, auth_headers):
    client.post(
        "/api/portfolios",
        json={
            "market": "美股",
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "shares": 25,
            "cost_price": 140.0,
        },
        headers=auth_headers,
    )
    response = client.get("/api/export/csv", headers=auth_headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"


def test_export_csv_with_market_filter(client, auth_headers):
    client.post(
        "/api/portfolios",
        json={
            "market": "A股",
            "symbol": "600519",
            "name": "贵州茅台",
            "shares": 50,
            "cost_price": 1800.0,
        },
        headers=auth_headers,
    )
    response = client.get("/api/export/csv?market=A股", headers=auth_headers)
    assert response.status_code == 200