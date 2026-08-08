"""レシピマスタのシード投入。"""

from sqlalchemy.orm import Session

from app.models import Recipe
from app.services.seed_data import SEED_RECIPES


def seed_recipes(db: Session) -> int:
    """既存のレシピを壊さず、未登録のレシピだけを追加する。"""
    existing = {r.name for r in db.query(Recipe.name).all()}
    added = 0
    for data in SEED_RECIPES:
        if data["name"] in existing:
            continue
        db.add(
            Recipe(
                name=data["name"],
                meal_type=data["meal_type"],
                ingredients=data["ingredients"],
                instructions=data["instructions"],
                cook_time_minutes=data["cook_time_minutes"],
            )
        )
        added += 1
    if added:
        db.commit()
    return added
