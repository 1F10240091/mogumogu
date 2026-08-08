"""献立テキストのパーサ。

OCR / PDF 抽出で得た献立表テキストを、日付と献立項目に構造化する。
保育園の献立表は「8/1(金) 昼食: ごはん・ハンバーグ・野菜スープ」のような
形式で記載されることが多いため、この形式に合わせて解析する。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_DATE_PATTERN = re.compile(r"(\d{1,2})[/.月](\d{1,2})日?(?:[\(（]\s*([月火水木金土日祝])\s*[\)）])?")
_LINE_SPLIT_PATTERN = re.compile(r"[・、,，\n\r\s]+")


@dataclass
class MenuEntry:
    """1 日分の献立項目。"""

    month: int | None = None
    day: int | None = None
    weekday: str | None = None
    raw_text: str = ""
    dishes: list[str] = field(default_factory=list)


def parse_menu_text(text: str, year: int | None = None) -> list[MenuEntry]:
    """献立テキストを日付ごとのエントリに分解する。

    Args:
        text: OCR / PDF 抽出結果のテキスト。
        year: 年（省略時は現在の年を使用）。保存時に日付を作るために使う。

    Returns:
        list[MenuEntry]: 日付ごとの献立エントリのリスト。
    """
    entries: list[MenuEntry] = []
    current: MenuEntry | None = None

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        match = _DATE_PATTERN.search(line)
        if match:
            if current is not None:
                entries.append(current)
            current = MenuEntry(
                month=int(match.group(1)),
                day=int(match.group(2)),
                weekday=match.group(3),
                raw_text=line,
            )
            dishes = _extract_dishes(line, match.end())
            current.dishes.extend(dishes)
        elif current is not None:
            current.raw_text += " " + line
            current.dishes.extend(_extract_dishes(line, 0))

    if current is not None:
        entries.append(current)

    return entries


def _extract_dishes(line: str, start: int) -> list[str]:
    """献立行から料理名を分解する。

    「8/1(金) 昼食: ごはん・ハンバーグ・野菜スープ」のような行から、
    区切り文字（・、/ 空白）で料理名を抽出する。
    """
    tail = line[start:].strip()
    # 「昼食:」「昼食：」のようなラベルを除去
    colon_match = re.match(r"^[^\s:：]*[:：]\s*", tail)
    if colon_match:
        tail = tail[colon_match.end():]
    else:
        # コロン無しの行は先頭の既知ラベル（昼食・夕食・給食・朝食・おやつ）のみ除去
        # そうしないと「8/3 ごはん みそ汁」の「ごはん」が消えてしまう。
        label_match = re.match(r"^(昼食|夕食|給食|朝食|おやつ|ランチ)\s*", tail)
        if label_match:
            tail = tail[label_match.end():]
    items = [item for item in _LINE_SPLIT_PATTERN.split(tail) if item]
    return items
