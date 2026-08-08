"""冷蔵庫の在庫・買い物リスト API。"""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import InventoryItem, Recipe, SuggestedMeal, User
from app.routers.auth import get_current_user
from app.services.shopping_list import ShoppingItem, build_shopping_list

router = APIRouter(prefix="/shopping", tags=["shopping"])


class ShoppingItemOut(BaseModel):
    name: str
    quantity: str | None = None
    unit: str = ""
    needed: str = ""
    source_recipes: list[str] = []


class InventoryItemOut(BaseModel):
    id: str
    name: str
    quantity: str | None = None


class ShoppingListResponse(BaseModel):
    items: list[ShoppingItemOut]
    generated_at: datetime


class InventoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    quantity: str | None = None


@router.get("/list", response_model=ShoppingListResponse)
def get_shopping_list(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ShoppingListResponse:
    """直近の提案献立に必要な食材から、在庫にあるものを除いた不足食材を返す。"""
    recent_meals = (
        db.query(SuggestedMeal)
        .filter(SuggestedMeal.user_id == user.id)
        .order_by(SuggestedMeal.date.desc())
        .limit(7)
        .all()
    )
    recipe_ids: list[str] = []
    for meal in recent_meals:
        ids = meal.ingredients.get("recipe_ids", []) if isinstance(meal.ingredients, dict) else []
        recipe_ids.extend(ids)

    if not recipe_ids:
        return ShoppingListResponse(items=[], generated_at=datetime.now(UTC))

    recipes_by_id = {r.id: r for r in db.query(Recipe).all()}
    inventory = [item.name for item in db.query(InventoryItem).filter(InventoryItem.user_id == user.id).all()]

    items = build_shopping_list(recipe_ids=recipe_ids, recipes_by_id=recipes_by_id, inventory=inventory)
    return ShoppingListResponse(
        items=[ShoppingItemOut(name=i.name, quantity=i.quantity, unit=i.unit, needed=i.needed, source_recipes=i.source_recipes) for i in items],
        generated_at=datetime.now(UTC),
    )


@router.post("/generate", response_model=ShoppingListResponse, status_code=status.HTTP_201_CREATED)
def generate_shopping_list(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> ShoppingListResponse:
    """買い物リストを再生成する（/list と同じロジック）。"""
    return get_shopping_list(user=user, db=db)


@router.get("/inventory", response_model=list[InventoryItemOut])
def list_inventory(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[InventoryItem]:
    return db.query(InventoryItem).filter(InventoryItem.user_id == user.id).all()


@router.post("/inventory", response_model=InventoryItemOut, status_code=status.HTTP_201_CREATED)
def add_inventory_item(
    payload: InventoryCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> InventoryItem:
    item = InventoryItem(user_id=user.id, name=payload.name, quantity=payload.quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/inventory/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(item_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id, InventoryItem.user_id == user.id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="在庫が見つかりません")
    db.delete(item)
    db.commit()
