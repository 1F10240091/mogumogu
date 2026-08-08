"""OCR サービス。

保育園から配布される献立表（PDF / 画像）からテキストを抽出する。
- PDF: pypdf によるテキスト抽出（デジタル生成の PDF 向け、OCR 不要）
- 画像: Gemini の OpenAI 互換 API（画像を base64 で渡して文字列化・遅延ロード）
- スキャン PDF: 各ページを画像化して Gemini で読み取る（全ページ対応）

API キー未設定時は画像系の抽出ができず、OCRProcessingError を返す。
"""

from __future__ import annotations

import base64
import io
from dataclasses import dataclass

import httpx

from app.config import get_settings

ALLOWED_PDF_TYPES = {"application/pdf"}
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}


class OCRUnsupportedError(ValueError):
    """対応していないファイル形式を受け取った場合のエラー。"""


class OCRProcessingError(RuntimeError):
    """OCR 処理中に失敗した場合のエラー。"""


@dataclass
class OCRResult:
    """OCR 抽出結果。"""

    text: str
    engine: str
    raw_pages: list[str] | None = None


def extract_text(filename: str, content_type: str, data: bytes) -> OCRResult:
    """ファイル内容からテキストを抽出する。

    Args:
        filename: アップロードされたファイル名。
        content_type: MIME タイプ。
        data: ファイルのバイト列。

    Returns:
        OCRResult: 抽出結果。

    Raises:
        OCRUnsupportedError: 対応形式でない場合。
        OCRProcessingError: 抽出処理に失敗した場合。
    """
    if content_type in ALLOWED_PDF_TYPES or filename.lower().endswith(".pdf"):
        return _extract_from_pdf(data)
    if content_type in ALLOWED_IMAGE_TYPES or _is_image_filename(filename):
        return _extract_from_image(data)
    raise OCRUnsupportedError(f"対応していないファイル形式です: {content_type or filename}")


def _is_image_filename(filename: str) -> bool:
    return filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))


def _extract_from_pdf(data: bytes) -> OCRResult:
    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(data))
        pages = [(page.extract_text() or "") for page in reader.pages]
        text = "\n".join(pages).strip()
    except Exception as exc:  # noqa: BLE001 - 原因に応じて変換する
        raise OCRProcessingError(f"PDF のテキスト抽出に失敗しました: {exc}") from exc

    if not text:
        # スキャン画像 PDF の場合、各ページを画像として OCR を試みる。
        return _extract_from_scan_pdf(data, page_count=len(reader.pages))
    return OCRResult(text=text, engine="pypdf", raw_pages=pages)


def _extract_from_scan_pdf(data: bytes, page_count: int) -> OCRResult:
    """スキャン PDF の全ページを画像化して OCR する。"""
    try:
        import pypdfium2 as pdfium
    except ImportError as exc:
        raise OCRProcessingError(
            "スキャン PDF の読み取りには pypdfium2 が必要です。"
            " `pip install pypdfium2` を実行してください。"
        ) from exc

    try:
        pdf = pdfium.PdfDocument(data)
        results: list[str] = []
        for i in range(len(pdf)):
            page = pdf[i]
            bitmap = page.render(scale=200 / 72, rotation=0)  # 200 DPI 相当
            pil_image = bitmap.to_pil()
            result = _extract_from_image(pil_image)
            results.append(result.text)
    except OCRProcessingError:
        # _extract_from_image 由来のエラー（APIキー未設定等）はそのまま伝える
        raise
    except Exception as exc:  # noqa: BLE001
        raise OCRProcessingError(f"PDF の画像変換に失敗しました: {exc}") from exc

    text = "\n".join(r for r in results if r).strip()
    if not text:
        return OCRResult(text="(スキャン画像からはテキストを抽出できませんでした)", engine="gemini")
    return OCRResult(text=text, engine="gemini", raw_pages=results)


def _extract_from_image(image_input) -> OCRResult:
    """画像（PIL Image または bytes）を Gemini で OCR する（遅延呼び出し）。"""
    settings = get_settings()
    if not settings.ai_api_key:
        raise OCRProcessingError(
            "画像 OCR には AI_API_KEY の設定が必要です。backend/.env に AI_API_KEY を設定してください。"
            " デジタル PDF は設定不要でそのまま読み取れます。"
        )

    # 入力（PIL Image / bytes）を JPEG のバイト列に統一する
    try:
        from PIL import Image

        if isinstance(image_input, bytes):
            image = Image.open(io.BytesIO(image_input))
        else:
            image = image_input
        if image.mode != "RGB":
            image = image.convert("RGB")
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        img_bytes = buf.getvalue()
    except Exception as exc:  # noqa: BLE001
        raise OCRProcessingError(f"画像の変換に失敗しました: {exc}") from exc

    prompt = (
        "保育園の献立表です。画像内の日付・曜日・料理名などを漏れなく日本語で抽出してください。\n"
        "段落や並び・行の区切りは改行で表現してください。料理名は『・』で区切ってください。\n"
        "画像中にテキストが無い場合は空文字列を返してください。"
    )
    payload = {
        "model": settings.ai_model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(img_bytes).decode()}"},
                    },
                ],
            }
        ],
    }
    headers = {
        "Authorization": f"Bearer {settings.ai_api_key}",
        "Content-Type": "application/json",
    }
    try:
        with httpx.Client(timeout=settings.ai_timeout_seconds) as client:
            resp = client.post(f"{settings.ai_base_url.rstrip('/')}/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
    except httpx.HTTPError as exc:
        raise OCRProcessingError(f"AI 画像読み取りに失敗しました: {exc}") from exc
    except (KeyError, IndexError) as exc:
        raise OCRProcessingError("AI の応答が不正です") from exc

    text = "\n".join(line.strip() for line in content.splitlines() if line.strip())
    return OCRResult(text=text, engine="gemini")