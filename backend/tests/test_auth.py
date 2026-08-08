"""認証 API のテスト。"""


def test_register_and_login(client):
    res = client.post("/api/v1/auth/register", json={"email": "u1@example.com", "password": "password123"})
    assert res.status_code == 201
    assert "access_token" in res.json()

    res = client.post("/api/v1/auth/login", json={"email": "u1@example.com", "password": "password123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_register_duplicate(client):
    client.post("/api/v1/auth/register", json={"email": "u2@example.com", "password": "password123"})
    res = client.post("/api/v1/auth/register", json={"email": "u2@example.com", "password": "password123"})
    assert res.status_code == 409


def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={"email": "u3@example.com", "password": "password123"})
    res = client.post("/api/v1/auth/login", json={"email": "u3@example.com", "password": "wrongpass"})
    assert res.status_code == 401


def test_me_requires_auth(client):
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401
