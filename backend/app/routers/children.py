"""お子様管理 API（登録・一覧・更新・削除）。"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Allergy, Child, Preference, User
from app.routers.auth import get_current_user
from app.schemas import AllergyCreate, ChildCreate, ChildResponse, ChildUpdate, PreferenceCreate

router = APIRouter(prefix="/children", tags=["children"])


@router.get("", response_model=list[ChildResponse])
def list_children(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Child]:
    return db.query(Child).filter(Child.user_id == user.id).all()


@router.post("", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
def create_child(payload: ChildCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Child:
    child = Child(user_id=user.id, name=payload.name, birth_date=payload.birth_date)
    child.allergies = [Allergy(ingredient=a.ingredient) for a in payload.allergies]
    child.preferences = [Preference(ingredient=p.ingredient, mode=p.mode) for p in payload.preferences]
    db.add(child)
    db.commit()
    db.refresh(child)
    return child


@router.get("/{child_id}", response_model=ChildResponse)
def get_child(child_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Child:
    child = _get_owned_child(db, user.id, child_id)
    return child


@router.put("/{child_id}", response_model=ChildResponse)
def update_child(
    child_id: str, payload: ChildUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Child:
    child = _get_owned_child(db, user.id, child_id)
    if payload.name is not None:
        child.name = payload.name
    if payload.birth_date is not None:
        child.birth_date = payload.birth_date
    db.commit()
    db.refresh(child)
    return child


@router.delete("/{child_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_child(child_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    child = _get_owned_child(db, user.id, child_id)
    db.delete(child)
    db.commit()


@router.post("/{child_id}/allergies", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
def add_allergy(
    child_id: str, payload: AllergyCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Child:
    child = _get_owned_child(db, user.id, child_id)
    ingredient = payload.ingredient.strip()
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="食材名を入力してください")
    if not any(a.ingredient == ingredient for a in child.allergies):
        child.allergies.append(Allergy(ingredient=ingredient))
    db.commit()
    db.refresh(child)
    return child


@router.delete("/{child_id}/allergies/{allergy_id}", response_model=ChildResponse)
def delete_allergy(
    child_id: str, allergy_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Child:
    child = _get_owned_child(db, user.id, child_id)
    allergy = db.query(Allergy).filter(Allergy.id == allergy_id, Allergy.child_id == child.id).first()
    if allergy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="アレルギーが見つかりません")
    db.delete(allergy)
    db.commit()
    db.refresh(child)
    return child


@router.post("/{child_id}/preferences", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
def add_preference(
    child_id: str, payload: PreferenceCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Child:
    child = _get_owned_child(db, user.id, child_id)
    ingredient = payload.ingredient.strip()
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="食材名を入力してください")
    if payload.mode not in ("exclude", "improve"):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="mode は exclude または improve です")
    if not any(p.ingredient == ingredient for p in child.preferences):
        child.preferences.append(Preference(ingredient=ingredient, mode=payload.mode))
    db.commit()
    db.refresh(child)
    return child


@router.delete("/{child_id}/preferences/{preference_id}", response_model=ChildResponse)
def delete_preference(
    child_id: str, preference_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Child:
    child = _get_owned_child(db, user.id, child_id)
    preference = db.query(Preference).filter(Preference.id == preference_id, Preference.child_id == child.id).first()
    if preference is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="好み設定が見つかりません")
    db.delete(preference)
    db.commit()
    db.refresh(child)
    return child


def _get_owned_child(db: Session, user_id: str, child_id: str) -> Child:
    child = db.query(Child).filter(Child.id == child_id, Child.user_id == user_id).first()
    if child is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="お子様が見つかりません")
    return child
