"""お子様管理 API のテスト。"""

from fastapi.testclient import TestClient

from app.main import app


def test_create_and_list_children(auth_client):
    res = auth_client.post(
        "/api/v1/children",
        json={"name": "ゆうた", "birth_date": "2021-04-01", "allergies": [{"ingredient": "卵"}], "preferences": []},
    )
    assert res.status_code == 201
    child_id = res.json()["id"]

    res = auth_client.get("/api/v1/children")
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["allergies"][0]["ingredient"] == "卵"


def test_add_and_delete_allergy(auth_client):
    res = auth_client.post("/api/v1/children", json={"name": "さくら", "allergies": [], "preferences": []})
    child_id = res.json()["id"]

    res = auth_client.post(f"/api/v1/children/{child_id}/allergies", json={"ingredient": "さけ"})
    assert res.status_code == 201
    assert [a["ingredient"] for a in res.json()["allergies"]] == ["さけ"]

    allergy_id = res.json()["allergies"][0]["id"]
    res = auth_client.delete(f"/api/v1/children/{child_id}/allergies/{allergy_id}")
    assert res.status_code == 200
    assert res.json()["allergies"] == []


def test_add_preference_validate_mode(auth_client):
    res = auth_client.post("/api/v1/children", json={"name": "ひなた", "allergies": [], "preferences": []})
    child_id = res.json()["id"]

    res = auth_client.post(f"/api/v1/children/{child_id}/preferences", json={"ingredient": "きのこ", "mode": "invalid"})
    assert res.status_code == 422


def test_cannot_access_other_users_child(client, auth_client):
    other_client = TestClient(app)
    res = other_client.post(
        "/api/v1/auth/register", json={"email": "other@example.com", "password": "password123"}
    )
    other_token = res.json()["access_token"]
    other_client.headers.update({"Authorization": f"Bearer {other_token}"})
    res = other_client.post("/api/v1/children", json={"name": "たろう", "allergies": [], "preferences": []})
    other_child_id = res.json()["id"]

    # 別ユーザーが他人の子にアクセスできないこと
    res = auth_client.get(f"/api/v1/children/{other_child_id}")
    assert res.status_code == 404
