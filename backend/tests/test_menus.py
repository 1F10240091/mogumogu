"""献立表（OCR・メニュー）API のテスト。"""

from io import BytesIO
from pathlib import Path

from app.services.menu_parser import parse_menu_text

SAMPLE_PDF = Path(__file__).resolve().parent / "sample_menu.pdf"


def test_create_and_get_menu(auth_client):
    res = auth_client.post(
        "/api/v1/menus",
        json={"date": "2026-08-03", "menu_text": "月曜日: ごはん みそ汁 鶏の唐揚げ"},
    )
    assert res.status_code == 201
    menu_id = res.json()["id"]

    res = auth_client.get(f"/api/v1/menus/{menu_id}")
    assert res.status_code == 200
    assert res.json()["date"] == "2026-08-03"


def test_list_menus_empty(auth_client):
    res = auth_client.get("/api/v1/menus")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_upload_unsupported_type_rejected(auth_client):
    res = auth_client.post(
        "/api/v1/menus/upload",
        files={"file": ("menu.txt", b"text", "text/plain")},
    )
    assert res.status_code == 415


def test_upload_corrupt_pdf_rejected(auth_client):
    res = auth_client.post(
        "/api/v1/menus/upload",
        files={"file": ("menu.pdf", b"not a real pdf", "application/pdf")},
    )
    assert res.status_code in (415, 422)


def test_get_unknown_menu_404(auth_client):
    res = auth_client.get("/api/v1/menus/unknown-id")
    assert res.status_code == 404


def test_upload_valid_pdf(auth_client):
    """テキスト埋め込み PDF の OCR 抽出が成功することを確認する回帰テスト。"""
    if not SAMPLE_PDF.exists():
        return  # 実 PDF が無い環境ではスキップ
    data = SAMPLE_PDF.read_bytes()
    res = auth_client.post(
        "/api/v1/menus/upload",
        files={"file": ("sample_menu.pdf", data, "application/pdf")},
    )
    assert res.status_code == 201
    assert res.json()["menu_text"]
    assert len(res.json()["ingredients"]["dishes"]) > 0


def test_upload_pdf_stores_dishes_by_date(auth_client):
    """アップロードした献立表が日付別の料理名として構造化保存されることを確認する。"""
    if not SAMPLE_PDF.exists():
        return
    data = SAMPLE_PDF.read_bytes()
    res = auth_client.post(
        "/api/v1/menus/upload",
        files={"file": ("menu_aug.pdf", data, "application/pdf")},
    )
    assert res.status_code == 201
    by_date = res.json()["ingredients"]["dishes_by_date"]
    assert len(by_date) >= 1
    entry = by_date[0]
    assert entry["month"] == 8
    assert entry["day"] == 1
    assert "ハンバーグ" in entry["dishes"]


def test_parse_menu_text_multi_day():
    """複数日の献立テキストが日付ごとに分割されることを確認する。"""
    text = (
        "8/3(月) 昼食: ごはん みそ汁 ハンバーグ\n"
        "8/4(火) 昼食: ごはん みそ汁 焼き魚\n"
    )
    entries = parse_menu_text(text)
    assert len(entries) == 2
    assert (entries[0].month, entries[0].day) == (8, 3)
    assert "ハンバーグ" in entries[0].dishes
    assert (entries[1].month, entries[1].day) == (8, 4)
    assert "焼き魚" in entries[1].dishes
