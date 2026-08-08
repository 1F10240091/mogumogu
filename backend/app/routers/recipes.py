"""AI 献立提案 API。

保育園の昼食・冷蔵庫の在庫・アレルギー・好き嫌い・前日の夕食を考慮した
夕食献立を生成する。AI エンジンは Gemini（OpenAI 互換 API）を使用し、
API キー未設定時はルールベースにフォールバックする。
"""

from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Child, InventoryItem, NurseryMenu, Recipe, SuggestedMeal, User
from app.routers.auth import get_current_user
from app.schemas import GenerateRequest, GenerateResponse, MealResponse
from app.services.menu_generator import generate_menus

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("", response_model=list[MealResponse])
def list_recipes(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[SuggestedMeal]:
    return db.query(SuggestedMeal).filter(SuggestedMeal.user_id == user.id).order_by(SuggestedMeal.date.desc()).all()


@router.post("/generate", response_model=GenerateResponse, status_code=status.HTTP_201_CREATED)
def generate_recipe(
    payload: GenerateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> GenerateResponse:
    child = db.query(Child).filter(Child.id == payload.child_id, Child.user_id == user.id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="お子様が見つかりません")

    allergies = [a.ingredient for a in child.allergies]
    preferences = [p.ingredient for p in child.preferences if p.mode == "exclude"]

    end_date = payload.menu_date + timedelta(days=payload.days - 1)
    nursery_menus = [
        m.menu_text
        for m in db.query(NurseryMenu)
        .filter(NurseryMenu.user_id == user.id, NurseryMenu.date >= payload.menu_date, NurseryMenu.date <= end_date)
        .all()
    ]
    inventory = [item.name for item in db.query(InventoryItem).filter(InventoryItem.user_id == user.id).all()]

    # 各日の給食と被らない献立選定用に、日付→料理名リストを構築
    nursery_menus_by_date: dict[date, list[str]] = {}
    for m in db.query(NurseryMenu).filter(NurseryMenu.user_id == user.id).all():
        by_date = (m.ingredients or {}).get("dishes_by_date") or []
        if not by_date:
            continue
        for entry in by_date:
            day = entry.get("day")
            if not day:
                continue
            try:
                d = date(m.date.year, entry.get("month") or m.date.month, day)
            except (TypeError, ValueError):
                continue
            dishes = entry.get("dishes") or []
            nursery_menus_by_date.setdefault(d, []).extend(dishes)

    # レシピマスタを DB から取得（アレルゲン照合・選定の真実源）
    recipes = db.query(Recipe).all()

    # 前日の夕食を取得（週の境目をまたぐ場合も重複を避けるため開始日前日の献立を探す）
    yesterday = (
        db.query(SuggestedMeal)
        .filter(SuggestedMeal.user_id == user.id, SuggestedMeal.date < payload.menu_date)
        .order_by(SuggestedMeal.date.desc())
        .first()
    )
    yesterday_menu = yesterday.menu_text if yesterday else None

    generated = generate_menus(
        child_name=child.name,
        start_date=payload.menu_date,
        days=payload.days,
        allergies=allergies,
        preferences=preferences,
        nursery_menus=nursery_menus,
        yesterday_menu=yesterday_menu,
        inventory=inventory,
        recipes=recipes,
        nursery_menus_by_date=nursery_menus_by_date,
    )

    meals: list[SuggestedMeal] = []
    for menu in generated:
        meal = SuggestedMeal(
            user_id=user.id,
            date=menu.date,
            menu_text=menu.menu_text,
            ingredients={"dishes": menu.dishes, "engine": menu.engine, "recipe_ids": menu.recipe_ids},
        )
        db.add(meal)
        meals.append(meal)
    db.commit()
    for meal in meals:
        db.refresh(meal)

    return GenerateResponse(meals=meals)


@router.get("/{meal_id}", response_model=MealResponse)
def get_recipe(meal_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> SuggestedMeal:
    meal = db.query(SuggestedMeal).filter(SuggestedMeal.id == meal_id, SuggestedMeal.user_id == user.id).first()
    if meal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="提案献立が見つかりません")
    return meal
