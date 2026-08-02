import json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import Integer, func, or_, select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/recipes", tags=["recipes"])


def _parse_json_field(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except Exception:
        return []
    if not isinstance(parsed, list):
        return []
    return [str(item) for item in parsed]


def _serialize_recipe(recipe: models.Recipe) -> schemas.RecipeResponse:
    return schemas.RecipeResponse(
        id=recipe.id,
        title=recipe.title,
        description=recipe.description,
        category=schemas.RecipeCategory(recipe.category),
        ingredients=_parse_json_field(recipe.ingredients),
        instructions=_parse_json_field(recipe.instructions),
        cooking_time_minutes=(
            int(recipe.cooking_time_minutes) if recipe.cooking_time_minutes else None
        ),
        servings=int(recipe.servings) if recipe.servings else None,
        image_url=recipe.image_url,
        source_url=recipe.source_url,
        tags=_parse_json_field(recipe.tags),
        created_at=recipe.created_at,
        is_public=recipe.is_public == "true",
    )


@router.get("", response_model=schemas.RecipeSearchResponse)
def search_recipes(
    keyword: str | None = Query(None, description="Search keyword for title/description"),
    category: schemas.RecipeCategory | None = Query(None, description="Recipe category"),
    ingredients: list[str] | None = Query(None, description="Ingredients to include"),
    tags: list[str] | None = Query(None, description="Tags to filter"),
    max_cooking_time: int | None = Query(None, description="Maximum cooking time in minutes"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
) -> schemas.RecipeSearchResponse:
    query = select(models.Recipe).where(models.Recipe.is_public == "true")

    if keyword:
        keyword_filter = f"%{keyword}%"
        query = query.where(
            or_(
                models.Recipe.title.ilike(keyword_filter),
                models.Recipe.description.ilike(keyword_filter),
            )
        )

    if category:
        query = query.where(models.Recipe.category == category.value)

    if ingredients:
        for ingredient in ingredients:
            ingredient_filter = f"%{ingredient}%"
            query = query.where(models.Recipe.ingredients.ilike(ingredient_filter))

    if tags:
        for tag in tags:
            tag_filter = f"%{tag}%"
            query = query.where(models.Recipe.tags.ilike(tag_filter))

    if max_cooking_time:
        query = query.where(models.Recipe.cooking_time_minutes.cast(Integer) <= max_cooking_time)

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0

    query = query.order_by(models.Recipe.created_at.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    recipes = db.execute(query).scalars().all()

    return schemas.RecipeSearchResponse(
        recipes=[_serialize_recipe(r) for r in recipes],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=(total + per_page - 1) // per_page,
    )


@router.get("/{recipe_id}", response_model=schemas.RecipeResponse)
def get_recipe(recipe_id: UUID, db: Session = Depends(get_db)) -> schemas.RecipeResponse:
    recipe = db.get(models.Recipe, recipe_id)
    if not recipe or recipe.is_public != "true":
        raise HTTPException(status_code=404, detail="Recipe not found")
    return _serialize_recipe(recipe)


@router.post("", response_model=schemas.RecipeResponse, status_code=201)
def create_recipe(
    recipe: schemas.RecipeCreate, db: Session = Depends(get_db)
) -> schemas.RecipeResponse:
    db_recipe = models.Recipe(
        title=recipe.title,
        description=recipe.description,
        category=recipe.category.value,
        ingredients=json.dumps(recipe.ingredients, ensure_ascii=False),
        instructions=json.dumps(recipe.instructions, ensure_ascii=False),
        cooking_time_minutes=(
            str(recipe.cooking_time_minutes) if recipe.cooking_time_minutes else None
        ),
        servings=str(recipe.servings) if recipe.servings else None,
        image_url=recipe.image_url,
        source_url=recipe.source_url,
        tags=json.dumps(recipe.tags, ensure_ascii=False),
        is_public="true",
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return _serialize_recipe(db_recipe)


@router.patch("/{recipe_id}", response_model=schemas.RecipeResponse)
def update_recipe(
    recipe_id: UUID,
    recipe_update: schemas.RecipeUpdate,
    db: Session = Depends(get_db),
) -> schemas.RecipeResponse:
    recipe = db.get(models.Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    update_data = recipe_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field in ["ingredients", "instructions", "tags"] and value is not None:
            value = json.dumps(value, ensure_ascii=False)
        elif field in ["cooking_time_minutes", "servings"] and value is not None:
            value = str(value)
        elif field == "category" and value is not None:
            value = value.value
        elif field == "is_public" and value is not None:
            value = "true" if value else "false"
        setattr(recipe, field, value)

    db.commit()
    db.refresh(recipe)
    return _serialize_recipe(recipe)


@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: UUID, db: Session = Depends(get_db)) -> None:
    recipe = db.get(models.Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
