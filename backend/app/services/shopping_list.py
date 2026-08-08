"""買い物リスト生成サービス。

献立に含まれるレシピの使用食品を集計し、冷蔵庫の在庫にある食材を
差し引いた不足食材リストを生成する。同じ食材が複数のレシピで使われる
場合は分量を合計して「必要合計分量」として表示する（調味料を除く）。
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field

# 合計分量を算出しない（表示しない）調味料（部分一致で判定）
SEASONINGS = {
    "しょうゆ", "醤油", "味噌", "みそ", "砂糖", "塩", "みりん", "料理酒", "酒",
    "酢", "ケチャップ", "マヨネーズ", "コンソメ", "だし", "カレールー",
    "ハヤシルー", "オイスターソース", "ソース", "こしょう", "胡椒",
    "ごま油", "サラダ油", "揚げ油", "オリーブ油", "片栗粉", "カレー粉",
    "からし", "辛子", "わさび", "ポン酢", "みそだれ", "ドレッ",
}


@dataclass
class ShoppingItem:
    """不足食材 1 件。"""

    name: str
    quantity: str = ""
    unit: str = ""
    needed: str = ""
    source_recipes: list[str] = field(default_factory=list)


def _to_float(value: str) -> float | None:
    """整数・小数・分数の文字列を数値に変換する。変換できない場合は None。"""
    s = value.strip()
    if re.fullmatch(r"\d+(\.\d+)?", s):
        return float(s)
    m = re.fullmatch(r"(\d+)\s*[/／]\s*(\d+)", s)
    if m:
        try:
            return float(m.group(1)) / float(m.group(2))
        except ZeroDivisionError:
            return None
    return None


def _parse_amount(ing: dict) -> tuple[float | None, str]:
    """食材 1 件から（数値, 単位）を取り出す。

    データ上 quantity / unit のどちらに数値が入るかは不規則のため、
    数値（整数・小数・分数）を含む側を値、もう片方を単位として解釈する。
    """
    q = str(ing.get("quantity", "") or "").strip()
    u = str(ing.get("unit", "") or "").strip()
    q_num = _to_float(q)
    u_num = _to_float(u)
    if q_num is not None and u_num is not None:
        return q_num, u
    if q_num is not None:
        return q_num, u
    if u_num is not None:
        return u_num, q
    return None, f"{q} {u}".strip()


def _is_seasoning(name: str) -> bool:
    lowered = name.lower()
    return any(key in lowered for key in SEASONINGS)


def _measure(ing: dict) -> str:
    """食材 1 件を "数値 単位" へ。数値が無ければ元の "quantity unit" 表記。"""
    num, unit = _parse_amount(ing)
    if num is not None:
        return f"{num:g} {unit}".strip()
    return f"{ing.get('quantity','')} {ing.get('unit','')}".strip()


def _summarize(ings: list[dict]) -> str:
    """複数レシピでの同食材の分量を合計した表示を返す。

    数値として解釈できるものは足し合わせ、できないもの（適量・少々など）は
    そのまま併記する。
    """
    if not ings:
        return ""
    total: float = 0.0
    unit: str = ""
    unparsed: list[str] = []
    for ing in ings:
        num, un = _parse_amount(ing)
        if num is None:
            unparsed.append(_measure(ing))
            continue
        total += num
        if not unit and un:
            unit = un
    parts = [f"{total:g} {unit}".strip()]
    if unparsed:
        parts.append(f"（その他 {'、'.join(dict.fromkeys(unparsed))}）")
    return " ・ ".join(parts)


def build_shopping_list(*, recipe_ids: list[str], recipes_by_id: dict[str, object], inventory: list[str]) -> list[ShoppingItem]:
    """指定されたレシピの食材から不足食材リストを生成する。

    Args:
        recipe_ids: 献立で使用するレシピ ID のリスト。
        recipes_by_id: レシピ ID をキーとするレシピの辞書。
        inventory: 冷蔵庫にある食材名のリスト。

    Returns:
        不足食材のリスト（在庫にある食材は除外済み）。
    """
    source_by_name: dict[str, list[str]] = defaultdict(list)
    raw_by_name: dict[str, list[dict]] = defaultdict(list)

    for recipe_id in recipe_ids:
        recipe = recipes_by_id.get(recipe_id)
        if recipe is None:
            continue
        recipe_name = getattr(recipe, "name", "?")
        for ing in getattr(recipe, "ingredients", []):
            name = ing.get("name", "")
            if not name:
                continue
            source_by_name[name].append(recipe_name)
            raw_by_name[name].append(ing)

    # 在庫にある食材を除外（表記ゆれ対応のため部分一致で判定）
    def in_inventory(name: str) -> bool:
        lowered = name.lower()
        return any(lowered in inv.lower() or inv.lower() in lowered for inv in inventory if inv)

    items: list[ShoppingItem] = []
    for name, ingredients in raw_by_name.items():
        if in_inventory(name):
            continue
        source_recipes = list(dict.fromkeys(source_by_name[name]))
        if _is_seasoning(name):
            # 調味料は合計せず最初の表記のみ
            needed = _measure(ingredients[0])
        else:
            needed = _summarize(ingredients)
        items.append(
            ShoppingItem(
                name=name,
                quantity=ingredients[0].get("quantity", ""),
                unit=ingredients[0].get("unit", ""),
                needed=needed,
                source_recipes=source_recipes,
            )
        )
    items.sort(key=lambda it: it.name)
    return items