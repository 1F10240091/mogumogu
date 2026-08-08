"""フィードバック API（ユーザーテスト・学祭アンケート収集）。"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])


class FeedbackCreate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: str = Field(default="", max_length=2000)


class FeedbackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    rating: int | None
    comment: str


@router.post("", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)) -> Feedback:
    if not payload.comment.strip() and payload.rating is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="評価またはコメントを入力してください")
    item = Feedback(rating=payload.rating, comment=payload.comment.strip())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[FeedbackResponse])
def list_feedback(db: Session = Depends(get_db)) -> list[Feedback]:
    return db.query(Feedback).order_by(Feedback.created_at.desc()).all()
