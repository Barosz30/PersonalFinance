from fastapi.testclient import TestClient


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_register_and_login(client: TestClient) -> None:
    r1 = client.post("/auth/register", json={"email": "demo@example.com", "password": "secret123"})
    assert r1.status_code == 201
    r2 = client.post("/auth/token", data={"username": "demo@example.com", "password": "secret123"})
    assert r2.status_code == 200
    assert "access_token" in r2.json()


def test_accounts_categories_transactions_and_reports(client: TestClient, token: str) -> None:
    headers = auth_headers(token)
    account = client.post("/accounts", json={"name": "Main", "balance": "1000.00"}, headers=headers).json()
    category = client.post("/categories", json={"name": "Food"}, headers=headers).json()

    tr = client.post(
        "/transactions",
        json={
            "amount": "55.20",
            "note": "Groceries",
            "booked_at": "2026-04-01",
            "type": "expense",
            "account_id": account["id"],
            "category_id": category["id"],
        },
        headers=headers,
    )
    assert tr.status_code == 201

    budget = client.post(
        "/budgets",
        json={"category_id": category["id"], "year": 2026, "month": 4, "limit_amount": "500.00"},
        headers=headers,
    )
    assert budget.status_code == 201

    report = client.get("/reports/monthly?year=2026&month=4", headers=headers)
    assert report.status_code == 200
    data = report.json()
    assert data["total_expense"] == "55.20"
    assert data["balance"] == "-55.20"

    csv_resp = client.get("/reports/monthly/csv?year=2026&month=4", headers=headers)
    assert csv_resp.status_code == 200
    assert "text/csv" in csv_resp.headers["content-type"]
