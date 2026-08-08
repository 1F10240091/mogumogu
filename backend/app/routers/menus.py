"""献立表 API（OCR 読み取り・一覧・詳細）。"""

from datetime import date

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.database import get_db
from app.models import NurseryMenu, User
from app.routers.auth import get_current_user
from app.schemas import NurseryMenuCreate, NurseryMenuResponse
from app.services.menu_parser import parse_menu_text
from app.services.ocr import OCRProcessingError, OCRUnsupportedError, extract_text

router = APIRouter(prefix="/menus", tags=["menus"])


@router.get("", response_model=list[NurseryMenuResponse])
def list_menus(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[NurseryMenu]:
    return db.query(NurseryMenu).filter(NurseryMenu.user_id == user.id).order_by(NurseryMenu.date.desc()).all()


@router.post("/upload", response_model=NurseryMenuResponse, status_code=status.HTTP_201_CREATED)
async def upload_menu(
    file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> NurseryMenu:
    """献立表の PDF/画像をアップロードし、OCR でテキスト化して保存する。

    抽出したテキストを日付・献立項目に構造化し、食材リストとして保存する。
    """
    MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20 MB
    data = await file.read()
    if len(data) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="ファイルサイズが大きすぎます（20MBまで）")
    try:
        result = await run_in_threadpool(
            extract_text,
            filename=file.filename or "",
            content_type=file.content_type or "",
            data=data,
        )
    except OCRUnsupportedError as exc:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=str(exc)) from exc
    except OCRProcessingError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    # 日付別に構造化して保存（各日の給食と被らない献立提案に利用）
    entries = parse_menu_text(result.text)
    dishes_by_date = [
        {
            "month": e.month,
            "day": e.day,
            "weekday": e.weekday,
            "dishes": e.dishes,
        }
        for e in entries
        if e.dishes
    ]
    dishes = _collect_dishes(result.text)
    menu = NurseryMenu(
        user_id=user.id,
        date=date.today(),
        menu_text=result.text,
        ingredients={
            "dishes": dishes,
            "dishes_by_date": dishes_by_date,
        },
    )
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


@router.post("", response_model=NurseryMenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(payload: NurseryMenuCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> NurseryMenu:
    menu = NurseryMenu(user_id=user.id, date=payload.date, menu_text=payload.menu_text, ingredients={})
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


@router.get("/{menu_id}", response_model=NurseryMenuResponse)
def get_menu(menu_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> NurseryMenu:
    menu = db.query(NurseryMenu).filter(NurseryMenu.id == menu_id, NurseryMenu.user_id == user.id).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="献立が見つかりません")
    return menu


def _collect_dishes(text: str) -> list[str]:
    """献立テキストから料理名のリストを収集する。"""
    dishes: list[str] = []
    for entry in parse_menu_text(text):
        for dish in entry.dishes:
            if dish not in dishes:
                dishes.append(dish)
    return dishes
