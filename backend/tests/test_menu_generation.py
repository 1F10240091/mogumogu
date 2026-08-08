"""AI 献立生成 API のテスト。"""


def test_generate_weekly_menu(auth_client):
    res = auth_client.post("/api/v1/children", json={"name": "ゆうた", "allergies": [{"ingredient": "卵"}], "preferences": []})
    child_id = res.json()["id"]

    res = auth_client.post(
        "/api/v1/recipes/generate", json={"child_id": child_id, "menu_date": "2026-08-03", "days": 5}
    )
    assert res.status_code == 201
    meals = res.json()["meals"]
    assert len(meals) == 5

    # 卵アレルギーのため、卵を含む料理名（和風ハンバーグ・オムライス）は選ばれない
    menus = " ".join(m["menu_text"] for m in meals)
    assert "オムライス" not in menus
    assert "和風ハンバーグ" not in menus


def test_generate_respects_days_limit(auth_client):
    res = auth_client.post("/api/v1/children", json={"name": "ひなた", "allergies": [], "preferences": []})
    child_id = res.json()["id"]

    res = auth_client.post(
        "/api/v1/recipes/generate", json={"child_id": child_id, "menu_date": "2026-08-03", "days": 8}
    )
    assert res.status_code == 422  # days は 1〜7 に制限


def test_generate_unknown_child(auth_client):
    res = auth_client.post(
        "/api/v1/recipes/generate", json={"child_id": "unknown-id", "menu_date": "2026-08-03", "days": 1}
    )
    assert res.status_code == 404


def test_generate_avoids_yesterday(auth_client):
    res = auth_client.post("/api/v1/children", json={"name": "ゆうた", "allergies": [], "preferences": []})
    child_id = res.json()["id"]

    # 日曜にカレーライスを生成
    res = auth_client.post(
        "/api/v1/recipes/generate", json={"child_id": child_id, "menu_date": "2026-08-02", "days": 1}
    )
    assert res.status_code == 201

    # 月曜開始の週間生成では主菜（カレーライス）が重複しない
    res = auth_client.post(
        "/api/v1/recipes/generate", json={"child_id": child_id, "menu_date": "2026-08-03", "days": 3}
    )
    monday_menu = res.json()["meals"][0]["menu_text"]
    assert "カレーライス" not in monday_menu


def test_generate_avoids_nursery_lunch_by_date(auth_client):
    """給食表をアップロードすると、各日の昼食と被らない夕食が生成されることを確認する。"""
    from pathlib import Path

    sample = Path(__file__).resolve().parent / "sample_menu.pdf"
    if not sample.exists():
        return

    # 給食表をアップロード（8/1 ハンバーグ・8/4 カレーライス・8/5 焼き魚）
    res = auth_client.post(
        "/api/v1/menus/upload",
        files={"file": ("menu.pdf", sample.read_bytes(), "application/pdf")},
    )
    assert res.status_code == 201

    res = auth_client.post("/api/v1/children", json={"name": "ゆうた", "allergies": [], "preferences": []})
    child_id = res.json()["id"]

    # 8/1 開始で生成すると、その日の給食（ハンバーグ）を夕食が避ける
    res = auth_client.post(
        "/api/v1/recipes/generate", json={"child_id": child_id, "menu_date": "2026-08-01", "days": 1}
    )
    assert res.status_code == 201
    dishes = res.json()["meals"][0]["ingredients"]["dishes"]
    assert "ハンバーグ" not in dishes

    # 8/4 開始ならその日の給食（カレーライス）を避ける
    res = auth_client.post(
        "/api/v1/recipes/generate", json={"child_id": child_id, "menu_date": "2026-08-04", "days": 1}
    )
    assert res.status_code == 201
    dishes = res.json()["meals"][0]["ingredients"]["dishes"]
    assert "カレーライス" not in dishes
