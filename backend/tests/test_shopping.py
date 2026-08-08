"""買い物リスト・冷蔵庫 API のテスト。"""


def test_add_and_list_inventory(auth_client):
    res = auth_client.post("/api/v1/shopping/inventory", json={"name": "玉ねぎ"})
    assert res.status_code == 201

    res = auth_client.get("/api/v1/shopping/inventory")
    assert res.status_code == 200
    assert any(i["name"] == "玉ねぎ" for i in res.json())


def test_shopping_list_excludes_inventory(auth_client):
    res = auth_client.post("/api/v1/children", json={"name": "ゆうた", "allergies": [], "preferences": []})
    child_id = res.json()["id"]

    auth_client.post("/api/v1/recipes/generate", json={"child_id": child_id, "menu_date": "2026-08-10", "days": 3})
    auth_client.post("/api/v1/shopping/inventory", json={"name": "みそ"})

    res = auth_client.get("/api/v1/shopping/list")
    assert res.status_code == 200
    names = [i["name"] for i in res.json()["items"]]
    assert "みそ" not in names
    assert len(names) > 0


def test_delete_inventory_item(auth_client):
    res = auth_client.post("/api/v1/shopping/inventory", json={"name": "じゃがいも"})
    item_id = res.json()["id"]

    res = auth_client.delete(f"/api/v1/shopping/inventory/{item_id}")
    assert res.status_code == 204

    res = auth_client.get("/api/v1/shopping/inventory")
    assert not any(i["name"] == "じゃがいも" for i in res.json())
