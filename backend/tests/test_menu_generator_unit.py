"""menu_generator サービスの単体テスト。"""

from datetime import date, timedelta

from app.models import Recipe
from app.services.menu_generator import (
    _matches_ingredient,
    _nursery_dishes_for_date,
    _recipe_has_allergen,
    _shared_names,
    generate_menus,
)


def _recipe(name: str, ingredients: list[dict]) -> Recipe:
    return Recipe(name=name, meal_type="main", ingredients=ingredients)


def test_matches_ingredient_synonyms():
    # 表記ゆれ（ひらがな⇔漢字⇔カタカナ）が一致する
    assert _matches_ingredient("さけ", "鮭の塩焼き")
    assert _matches_ingredient("卵", "だし巻き玉子")
    assert _matches_ingredient("大豆", "肉じゃが（みそ風味）")
    assert _matches_ingredient("牛乳", "バター炒め")
    # 一致しない場合
    assert not _matches_ingredient("卵", "鶏肉の唐揚げ")
    assert not _matches_ingredient("そば", "うどん")


def test_recipe_has_allergen():
    recipe = _recipe("オムライス", [{"name": "卵"}, {"name": "ケチャップ"}])
    assert _recipe_has_allergen(recipe, ["卵"])
    assert not _recipe_has_allergen(recipe, ["大豆"])

    safe = _recipe("肉じゃが", [{"name": "牛肉"}, {"name": "じゃがいも"}])
    assert not _recipe_has_allergen(safe, ["卵", "乳"])


def test_shared_names_ignores_basics():
    assert _shared_names(["カレーライス"], ["カレーライス"])
    # 基本の主食・汁物は重複判定の対象外
    assert not _shared_names(["ごはん"], ["ごはん"])
    assert not _shared_names(["みそ汁"], ["みそ汁"])
    assert not _shared_names(["カレーライス", "ごはん"], ["ハンバーグ", "ごはん"])


def test_nursery_dishes_for_date_exact():
    by_date = {date(2026, 8, 3): ["ごはん", "ハンバーグ"]}
    assert _nursery_dishes_for_date(by_date, date(2026, 8, 3)) == ["ごはん", "ハンバーグ"]


def test_nursery_dishes_for_date_fallback_to_previous():
    by_date = {date(2026, 8, 3): ["ごはん", "ハンバーグ"]}
    # 該当日が無い場合は直前の日付の給食を使う
    assert _nursery_dishes_for_date(by_date, date(2026, 8, 4)) == ["ごはん", "ハンバーグ"]


def test_nursery_dishes_for_date_empty():
    assert _nursery_dishes_for_date({}, date(2026, 8, 3)) == []


def test_generate_menus_avoids_daily_nursery_overlap():
    """その日の給食に含まれる主菜が夕食献立に選ばれないことを確認する。"""
    recipes = [
        Recipe(name="ハンバーグ", meal_type="main", ingredients=[{"name": "牛ひき肉"}]),
        Recipe(name="カレーライス", meal_type="main", ingredients=[{"name": "豚肉"}]),
        Recipe(name="みそ汁", meal_type="soup", ingredients=[{"name": "豆腐"}]),
        Recipe(name="ごはん", meal_type="staple", ingredients=[{"name": "米"}]),
    ]
    start = date(2026, 8, 3)
    by_date = {start: ["ごはん", "みそ汁", "ハンバーグ"]}

    menus = generate_menus(
        child_name="テスト子",
        start_date=start,
        days=1,
        allergies=[],
        preferences=[],
        nursery_menus=["ごはん みそ汁 ハンバーグ"],
        recipes=recipes,
        nursery_menus_by_date=by_date,
    )

    assert len(menus) == 1
    # 給食に含まれる「ハンバーグ」は夕食に選ばれない
    assert "ハンバーグ" not in menus[0].dishes
    assert any("カレーライス" == d for d in menus[0].dishes)


def test_generate_menus_avoids_partial_name_overlap():
    """給食「ハンバーグ」に対し「和風ハンバーグ」のような類似名も回避することを確認する。"""
    recipes = [
        Recipe(name="和風ハンバーグ", meal_type="main", ingredients=[{"name": "牛ひき肉"}]),
        Recipe(name="鮭の塩焼き", meal_type="main", ingredients=[{"name": "鮭"}]),
        Recipe(name="みそ汁", meal_type="soup", ingredients=[{"name": "豆腐"}]),
        Recipe(name="ごはん", meal_type="staple", ingredients=[{"name": "米"}]),
    ]
    start = date(2026, 8, 3)
    by_date = {start: ["ごはん", "みそ汁", "ハンバーグ"]}

    menus = generate_menus(
        child_name="テスト子",
        start_date=start,
        days=1,
        allergies=[],
        preferences=[],
        nursery_menus=["ごはん みそ汁 ハンバーグ"],
        recipes=recipes,
        nursery_menus_by_date=by_date,
    )

    assert len(menus) == 1
    # 給食の「ハンバーグ」を含む名前の主菜は夕食に選ばれない
    assert "和風ハンバーグ" not in menus[0].dishes
    assert "鮭の塩焼き" in menus[0].dishes


def test_generate_menus_multi_day_with_nursery():
    """複数日生成時に、日ごとの給食と被らない献立になることを確認する。"""
    recipes = [
        Recipe(name="ハンバーグ", meal_type="main", ingredients=[{"name": "牛ひき肉"}]),
        Recipe(name="カレーライス", meal_type="main", ingredients=[{"name": "豚肉"}]),
        Recipe(name="焼き魚", meal_type="main", ingredients=[{"name": "さば"}]),
        Recipe(name="みそ汁", meal_type="soup", ingredients=[{"name": "豆腐"}]),
        Recipe(name="ごはん", meal_type="staple", ingredients=[{"name": "米"}]),
    ]
    start = date(2026, 8, 3)
    by_date = {
        start: ["ごはん", "みそ汁", "ハンバーグ"],
        start + timedelta(days=1): ["ごはん", "みそ汁", "カレーライス"],
    }

    menus = generate_menus(
        child_name="テスト子",
        start_date=start,
        days=2,
        allergies=[],
        preferences=[],
        nursery_menus=["ごはん みそ汁 ハンバーグ"],
        recipes=recipes,
        nursery_menus_by_date=by_date,
    )

    assert len(menus) == 2
    # 1日目: 給食のハンバーグを回避
    assert "ハンバーグ" not in menus[0].dishes
    # 2日目: 給食のカレーライスを回避
    assert "カレーライス" not in menus[1].dishes
