"""AI 献立生成サービス。

レシピマスタ（DB）に登録された料理から、保育園の昼食・冷蔵庫の在庫・
アレルギー・好き嫌い・前日の夕食を考慮した夕食献立を選定する。

選定方式:
- Gemini（OpenAI 互換 API）が利用可能なら、レシピカタログと制約を
  渡して「どのレシピを選ぶか」を決めさせる。
- API キー未設定時はルールベースで DB から順に選定する。
- どちらの場合も選定結果を DB の食材情報と照合し、アレルゲンが
  含まれないことを最終確認する。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date, timedelta

import httpx

from app.config import get_settings
from app.models import Recipe


@dataclass
class GeneratedMenu:
    """1 日分の生成献立。"""

    date: date
    menu_text: str
    dishes: list[str] = field(default_factory=list)
    engine: str = "rule_based"
    recipe_ids: list[str] = field(default_factory=list)


# 表記ゆれ（ひらがな⇔漢字⇔カタカナ）の同義語辞書
_SYNONYMS: dict[str, list[str]] = {
    "さけ": ["さけ", "鮭", "サーモン", "しゃけ"],
    "卵": ["卵", "たまご", "玉子", "エッグ"],
    "牛乳": ["牛乳", "乳", "バター", "チーズ", "ヨーグルト"],
    "小麦": ["小麦", "うどん", "パン", "麺"],
    "そば": ["そば", "蕎麦"],
    "大豆": ["大豆", "豆腐", "みそ", "味噌", "しょうゆ", "醤油", "油揚げ"],
    "落花生": ["落花生", "ピーナッツ", "ぴーなっつ"],
    "くるみ": ["くるみ", "胡桃"],
    "ごま": ["ごま", "ゴマ", "胡麻"],
}

def _matches_ingredient(ingredient: str, target: str) -> bool:
    """食材名（表記ゆれ対応）が対象文字列に含まれるか判定する。"""
    aliases = _SYNONYMS.get(ingredient.lower(), [ingredient])
    return any(alias in target for alias in aliases)


def _recipe_has_allergen(recipe: Recipe, allergens: list[str]) -> bool:
    """レシピの使用食品にアレルゲンが含まれるか判定する。"""
    if not allergens:
        return False
    recipe_ingredients = " ".join(str(i.get("name", "")) for i in recipe.ingredients)
    return any(_matches_ingredient(a, recipe_ingredients) for a in allergens)


def _shared_names(a: list[str], b: list[str]) -> bool:
    """2 つの料理名リストに共通する主菜レベルの料理があるか判定する。"""
    ignore = {"ごはん", "白ごはん", "みそ汁", "味噌汁", "スープ", "おひたし"}
    sa = {d for d in a if d not in ignore}
    sb = {d for d in b if d not in ignore}
    return bool(sa & sb)


def _nursery_dishes_for_date(nursery_menus_by_date: dict[date, list[str]], d: date) -> list[str]:
    """指定日（または前日）の給食料理名リストを返す。

    日付のずれ（週末など）を考慮し、該当日が無い場合は直前の日付を探す。
    """
    if not nursery_menus_by_date:
        return []
    if d in nursery_menus_by_date:
        return nursery_menus_by_date[d]
    # 該当日が無い場合は直近の過去日を探索
    past = [k for k in nursery_menus_by_date if k <= d]
    if past:
        return nursery_menus_by_date[max(past)]
    return next(iter(nursery_menus_by_date.values()), [])


def generate_menus(
    *,
    child_name: str,
    start_date: date,
    days: int,
    allergies: list[str],
    preferences: list[str],
    nursery_menus: list[str],
    yesterday_menu: str | None = None,
    inventory: list[str] | None = None,
    recipes: list[Recipe] | None = None,
    nursery_menus_by_date: dict[date, list[str]] | None = None,
) -> list[GeneratedMenu]:
    """指定日数分の夕食献立をレシピマスタから選定する。

    Args:
        child_name: お子様の名前。
        start_date: 生成開始日。
        days: 生成する日数（1〜7）。
        allergies: アレルギー食材リスト。
        preferences: 好き嫌い（除外希望）リスト。
        nursery_menus: 保育園の昼食献立テキスト（重複回避用）。
        yesterday_menu: 前日の夕食献立テキスト。週の境目（日曜→月曜など）を
            またいでも漏れなく重複を避けるため、開始日前日の夕食を渡す。
        inventory: 冷蔵庫の在庫食材リスト。
        recipes: レシピマスタ。None の場合は DB から全件取得する。
        nursery_menus_by_date: 日付→給食料理名リストの対応（各日の給食と被らない
            献立選定に使用）。None の場合は従来どおりテキスト全体で重複回避する。

    Returns:
        日付ごとの GeneratedMenu のリスト。
    """
    settings = get_settings()
    inventory = inventory or []
    recipe_list = recipes if recipes is not None else []
    by_date = nursery_menus_by_date or {}

    if settings.ai_api_key:
        try:
            return _generate_with_ai(
                child_name=child_name,
                start_date=start_date,
                days=days,
                allergies=allergies,
                preferences=preferences,
                nursery_menus=nursery_menus,
                yesterday_menu=yesterday_menu,
                inventory=inventory,
                recipes=recipe_list,
            )
        except Exception:
            # AI 接続失敗時はルールベースにフォールバック
            pass

    return _generate_rule_based(
        child_name=child_name,
        start_date=start_date,
        days=days,
        allergies=allergies,
        preferences=preferences,
        nursery_menus=nursery_menus,
        yesterday_menu=yesterday_menu,
        recipes=recipe_list,
        nursery_menus_by_date=by_date,
    )


def _generate_rule_based(
    *,
    child_name: str,
    start_date: date,
    days: int,
    allergies: list[str],
    preferences: list[str],
    nursery_menus: list[str],
    yesterday_menu: str | None,
    recipes: list[Recipe],
    nursery_menus_by_date: dict[date, list[str]] | None = None,
) -> list[GeneratedMenu]:
    """レシピマスタからルールベースで献立を選定する。

    アレルギー・好き嫌いを除外し、保育園の昼食・前日の夕食・今週内の
    既選献立と主菜が重複しない組み合わせを順に選ぶ。
    """
    allergens = [a.lower() for a in allergies + preferences]
    nursery_text = " ".join(nursery_menus)
    yesterday_dishes = _extract_dishes(yesterday_menu) if yesterday_menu else []
    by_date = nursery_menus_by_date or {}

    mains = [r for r in recipes if r.meal_type == "main"]
    soup = next((r for r in recipes if r.meal_type == "soup" and not _recipe_has_allergen(r, allergens)), None)
    sides = [r for r in recipes if r.meal_type == "side" and not _recipe_has_allergen(r, allergens)]
    staple = next((r for r in recipes if r.meal_type == "staple" and not _recipe_has_allergen(r, allergens)), None)

    selected: list[list[Recipe]] = []
    nursery_parts = [p for p in nursery_text.split("・") if p]
    for main in mains:
        if _recipe_has_allergen(main, allergens):
            continue
        if any(_matches_ingredient(part, main.name) or _matches_ingredient(main.name, part) for part in nursery_parts):
            continue
        if _shared_names([main.name], yesterday_dishes):
            continue
        if any(_shared_names([main.name], [prev[0].name]) for prev in selected):
            continue
        combo = [main]
        if soup:
            combo.append(soup)
        if sides:
            combo.append(sides[len(selected) % len(sides)])
        if staple and staple.name != main.name:
            combo.append(staple)
        selected.append(combo)

    if not selected:
        # すべての主菜が使えない場合は、アレルゲン判定済みの最小構成で代替
        fallback = [r for r in recipes if not _recipe_has_allergen(r, allergens)]
        combo = [fallback[0]] if fallback else []
        selected = [combo] * days

    result: list[GeneratedMenu] = []
    for i in range(days):
        d = start_date + timedelta(days=i)
        combo = selected[i % len(selected)]
        # 各日の給食と被らないように、その日の給食と重複する料理は差し替える
        combo = _avoid_nursery_overlap(combo, _nursery_dishes_for_date(by_date, d), mains, allergens)
        dishes = [r.name for r in combo]
        result.append(
            GeneratedMenu(
                date=d,
                menu_text=f"{child_name} さんの夕食（{d}）\n{'・'.join(dishes)}",
                dishes=dishes,
                engine="rule_based",
                recipe_ids=[r.id for r in combo],
            )
        )
    return result


def _avoid_nursery_overlap(
    combo: list[Recipe], nursery_dishes: list[str], mains: list[Recipe], allergens: list[str]
) -> list[Recipe]:
    """その日の給食と主菜が被らないよう、主菜を差し替える。

    給食に含まれる料理名と一致する主菜は、別の主菜（既に組み合わせで使われて
    いないもの）へ差し替える。被っていなければそのまま返す。
    """
    if not nursery_dishes:
        return combo
    result = list(combo)
    for idx, recipe in enumerate(result):
        if recipe.meal_type != "main":
            continue
        if any(
            _matches_ingredient(part, recipe.name) or _matches_ingredient(recipe.name, part)
            for part in nursery_dishes
        ):
            used_names = {r.name for r in result}
            replacement = next(
                (m for m in mains if m.name not in used_names and not _recipe_has_allergen(m, allergens)),
                None,
            )
            if replacement:
                result[idx] = replacement
    return result


def _extract_dishes(menu_text: str) -> list[str]:
    """献立テキストから・区切りの料理名リストを取り出す。"""
    dishes: list[str] = []
    for line in menu_text.splitlines():
        line = line.strip()
        if not line or "：" in line:
            continue
        for part in line.split("・"):
            part = part.strip()
            if part and part not in dishes:
                dishes.append(part)
    return dishes


def _generate_with_ai(
    *,
    child_name: str,
    start_date: date,
    days: int,
    allergies: list[str],
    preferences: list[str],
    nursery_menus: list[str],
    yesterday_menu: str | None,
    inventory: list[str],
    recipes: list[Recipe],
) -> list[GeneratedMenu]:
    """Gemini（OpenAI 互換 API）にレシピカタログから選定させる。"""
    settings = get_settings()

    catalog = "\n".join(
        f"- {r.name}（{r.meal_type} / 使用食品: {', '.join(i.get('name', '') for i in r.ingredients)}）"
        for r in recipes
    )

    system_prompt = (
        "あなたは保育園に通う 3〜6 歳児を持つ保護者向けに、夕食献立を提案する栄養士です。\n"
        "与えられたレシピカタログの料理名だけを使って献立を選定してください。\n"
        "カタログに無い料理名を出力しないでください。\n"
        "必ず JSON 配列のみを出力してください。\n"
        "出力形式: [{\"date\": \"YYYY-MM-DD\", \"dishes\": [\"料理名1\", \"料理名2\"]}]\n"
        "1 日の献立は主菜・汁物・副菜・主食の組み合わせにしてください。\n"
        "冷蔵庫の在庫にある食材は積極的に使い、無駄なく買い物できる献立にします。\n"
        "栄養バランス（たんぱく質・野菜・炭水化物）が偏らないようにします。"
    )

    user_prompt = (
        f"お子様: {child_name}\n"
        f"対象期間: {start_date} から {days} 日分\n"
        f"アレルギー: {allergies or 'なし'}\n"
        f"好き嫌い（除外希望）: {preferences or 'なし'}\n"
        f"保育園の昼食: {' / '.join(nursery_menus) or 'なし'}\n"
        f"前日の夕食（重複禁止）: {yesterday_menu or 'なし'}\n"
        f"冷蔵庫の在庫: {inventory or 'なし'}\n"
        f"レシピカタログ:\n{catalog}\n"
        f"アレルゲンを避け、在庫を活用し、保育園の昼食・前日の夕食と主菜が重複しない"
        f"栄養バランスの良い献立を {days} 日分選定してください。"
    )

    payload = {
        "model": settings.ai_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_completion_tokens": 1024,
    }

    headers = {
        "Authorization": f"Bearer {settings.ai_api_key}",
        "Content-Type": "application/json",
    }

    with httpx.Client(timeout=settings.ai_timeout_seconds) as client:
        resp = client.post(f"{settings.ai_base_url.rstrip('/')}/chat/completions", headers=headers, json=payload)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]

    entries = _parse_ai_response(content)
    menus: list[GeneratedMenu] = []
    for i, entry in enumerate(entries[:days]):
        d = start_date + timedelta(days=i)
        dishes = [str(x) for x in entry.get("dishes", []) if x]
        # カタログに無い料理は除外し、DB のレシピと照合
        by_name = {r.name: r for r in recipes}
        combo = [by_name[d] for d in dishes if d in by_name]
        if not combo:
            continue
        safe_combo = [r for r in combo if not _recipe_has_allergen(r, [a.lower() for a in allergies + preferences])]
        if not safe_combo:
            continue
        menus.append(
            GeneratedMenu(
                date=d,
                menu_text=f"{child_name} さんの夕食（{d}）\n{'・'.join(r.name for r in safe_combo)}",
                dishes=[r.name for r in safe_combo],
                engine="gemini",
                recipe_ids=[r.id for r in safe_combo],
            )
        )
    if not menus:
        raise RuntimeError("AI の出力を解析できませんでした")
    return menus


def _parse_ai_response(content: str) -> list[dict]:
    """AI の出力から JSON 配列を抽出する。"""
    match = re.search(r"\[.*\]", content, re.DOTALL)
    if not match:
        return []
    try:
        data = json.loads(match.group(0))
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
    except json.JSONDecodeError:
        return []
    return []
