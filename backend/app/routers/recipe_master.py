"""レシピマスタ API（一覧・検索・作成・更新・削除）。

読み取り系（一覧・検索・詳細）はログイン不要で利用できる。
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Recipe
from app.routers.auth import get_current_user
from app.schemas import RecipeCreate, RecipeResponse, RecipeSearchResponse, RecipeUpdate

router = APIRouter(prefix="/recipe-master", tags=["recipe-master"])


@router.get("", response_model=list[RecipeResponse])
def list_recipes(
    meal_type: str | None = None, db: Session = Depends(get_db)
) -> list[Recipe]:
    query = db.query(Recipe)
    if meal_type:
        query = query.filter(Recipe.meal_type == meal_type)
    return query.order_by(Recipe.name).all()


@router.get("/search", response_model=RecipeSearchResponse)
def search_recipes(
    keyword: str | None = Query(default=None, description="レシピ名・作り方の部分一致検索"),
    meal_type: str | None = Query(default=None, description="main | side | soup | staple"),
    ingredient: str | None = Query(default=None, description="材料名の部分一致検索"),
    max_cook_time: int | None = Query(default=None, ge=1, description="最大調理時間（分）"),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> RecipeSearchResponse:
    query = db.query(Recipe)

    if keyword:
        like = f"%{keyword}%"
        query = query.filter(Recipe.name.like(like) | Recipe.instructions.like(like))
    if meal_type:
        query = query.filter(Recipe.meal_type == meal_type)
    if max_cook_time is not None:
        query = query.filter(Recipe.cook_time_minutes <= max_cook_time)

    recipes = query.order_by(Recipe.name).all()

    # 材料は JSON の Unicode エスケープで保存されるため LIKE 不可。
    # デコードしてから Python 側で部分一致フィルタする。
    if ingredient:
        needle = ingredient.lower()
        recipes = [
            r
            for r in recipes
            if any(needle in ing.get("name", "").lower() for ing in r.ingredients)
        ]

    total = len(recipes)
    total_pages = (total + per_page - 1) // per_page if total else 0
    start = (page - 1) * per_page
    page_items = recipes[start : start + per_page]

    return RecipeSearchResponse(
        recipes=[RecipeResponse.model_validate(r) for r in page_items],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
    )


@router.post("", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(payload: RecipeCreate, user=Depends(get_current_user), db: Session = Depends(get_db)) -> Recipe:
    if db.query(Recipe).filter(Recipe.name == payload.name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="同じ名前のレシピが既に存在します")
    recipe = Recipe(
        name=payload.name,
        meal_type=payload.meal_type,
        ingredients=[i.model_dump() for i in payload.ingredients],
        instructions=payload.instructions,
        cook_time_minutes=payload.cook_time_minutes,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: str, db: Session = Depends(get_db)) -> Recipe:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="レシピが見つかりません")
    return recipe


@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: str, payload: RecipeUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)
) -> Recipe:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="レシピが見つかりません")

    if payload.name is not None:
        recipe.name = payload.name
    if payload.meal_type is not None:
        recipe.meal_type = payload.meal_type
    if payload.ingredients is not None:
        recipe.ingredients = [i.model_dump() for i in payload.ingredients]
    if payload.instructions is not None:
        recipe.instructions = payload.instructions
    if payload.cook_time_minutes is not None:
        recipe.cook_time_minutes = payload.cook_time_minutes
    db.commit()
    db.refresh(recipe)
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="レシピが見つかりません")
    db.delete(recipe)
    db.commit()
