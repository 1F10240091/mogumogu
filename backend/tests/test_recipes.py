"""レシピマスタ API のテスト。"""


def test_seed_recipes_loaded(auth_client):
    res = auth_client.get("/api/v1/recipe-master")
    assert res.status_code == 200
    assert len(res.json()) > 0
    names = {r["name"] for r in res.json()}
    assert "ごはん" in names
    assert "みそ汁" in names


def test_create_and_get_recipe(auth_client):
    res = auth_client.post(
        "/api/v1/recipe-master",
        json={
            "name": "テストカレー",
            "meal_type": "main",
            "ingredients": [{"name": "豚肉", "quantity": "150", "unit": "g"}],
            "instructions": "煮る。",
            "cook_time_minutes": 30,
        },
    )
    assert res.status_code == 201
    recipe_id = res.json()["id"]

    res = auth_client.get(f"/api/v1/recipe-master/{recipe_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "テストカレー"


def test_duplicate_recipe_rejected(auth_client):
    auth_client.post("/api/v1/recipe-master", json={"name": "重複レシピ", "meal_type": "main"})
    res = auth_client.post("/api/v1/recipe-master", json={"name": "重複レシピ", "meal_type": "main"})
    assert res.status_code == 409


def test_update_recipe(auth_client):
    res = auth_client.post("/api/v1/recipe-master", json={"name": "更新テスト", "meal_type": "main"})
    recipe_id = res.json()["id"]

    res = auth_client.put(
        f"/api/v1/recipe-master/{recipe_id}",
        json={"name": "更新テスト改", "instructions": "炒める。", "cook_time_minutes": 15},
    )
    assert res.status_code == 200
    assert res.json()["name"] == "更新テスト改"
    assert res.json()["instructions"] == "炒める。"


def test_delete_recipe(auth_client):
    res = auth_client.post("/api/v1/recipe-master", json={"name": "削除テスト", "meal_type": "side"})
    recipe_id = res.json()["id"]

    res = auth_client.delete(f"/api/v1/recipe-master/{recipe_id}")
    assert res.status_code == 204

    res = auth_client.get(f"/api/v1/recipe-master/{recipe_id}")
    assert res.status_code == 404


def test_filter_by_meal_type(auth_client):
    res = auth_client.get("/api/v1/recipe-master?meal_type=main")
    assert res.status_code == 200
    assert len(res.json()) > 0
    assert all(r["meal_type"] == "main" for r in res.json())


# --- レシピ検索 ---


def test_search_recipes_by_keyword(auth_client):
    res = auth_client.get("/api/v1/recipe-master/search", params={"keyword": "ごはん"})
    assert res.status_code == 200
    body = res.json()
    assert body["total"] > 0
    assert any("ごはん" in r["name"] for r in body["recipes"])


def test_search_recipes_by_ingredient(auth_client):
    res = auth_client.get("/api/v1/recipe-master/search", params={"ingredient": "にんじん"})
    assert res.status_code == 200
    body = res.json()
    assert body["total"] > 0
    assert any(
        "にんじん" in (ing["name"] for ing in r["ingredients"]) or "にんじん" in str(r["ingredients"])
        for r in body["recipes"]
    )


def test_search_recipes_by_max_cook_time(auth_client):
    res = auth_client.get("/api/v1/recipe-master/search", params={"max_cook_time": 10})
    assert res.status_code == 200
    body = res.json()
    for r in body["recipes"]:
        if r["cook_time_minutes"] is not None:
            assert r["cook_time_minutes"] <= 10


def test_search_recipes_pagination(auth_client):
    res = auth_client.get("/api/v1/recipe-master/search", params={"per_page": 5, "page": 1})
    assert res.status_code == 200
    body = res.json()
    assert len(body["recipes"]) <= 5
    assert body["total"] >= 1
    assert body["total_pages"] >= 1


def test_search_recipes_combined_filters(auth_client):
    res = auth_client.get(
        "/api/v1/recipe-master/search",
        params={"meal_type": "main", "keyword": "カレー"},
    )
    assert res.status_code == 200
    body = res.json()
    assert all(r["meal_type"] == "main" for r in body["recipes"])


def test_search_recipes_no_match(auth_client):
    res = auth_client.get(
        "/api/v1/recipe-master/search", params={"keyword": "存在しないレシピXYZ123"}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["total"] == 0
    assert body["recipes"] == []
