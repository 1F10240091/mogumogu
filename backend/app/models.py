"""データベースモデル定義。"""

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, JSON, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    children: Mapped[list["Child"]] = relationship(back_populates="user")


class Child(Base):
    __tablename__ = "children"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="children")
    allergies: Mapped[list["Allergy"]] = relationship(back_populates="child", cascade="all, delete-orphan")
    preferences: Mapped[list["Preference"]] = relationship(back_populates="child", cascade="all, delete-orphan")


class Allergy(Base):
    __tablename__ = "allergies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    child_id: Mapped[str] = mapped_column(ForeignKey("children.id"), index=True, nullable=False)
    ingredient: Mapped[str] = mapped_column(String(100), nullable=False)

    child: Mapped[Child] = relationship(back_populates="allergies")


class Preference(Base):
    __tablename__ = "preferences"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    child_id: Mapped[str] = mapped_column(ForeignKey("children.id"), index=True, nullable=False)
    ingredient: Mapped[str] = mapped_column(String(100), nullable=False)
    mode: Mapped[str] = mapped_column(String(20), nullable=False, default="exclude")  # exclude | improve

    child: Mapped[Child] = relationship(back_populates="preferences")


class NurseryMenu(Base):
    __tablename__ = "nursery_menus"
    __table_args__ = (Index("ix_nursery_menus_user_date", "user_id", "date"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    menu_text: Mapped[str] = mapped_column(Text, nullable=False)
    ingredients: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[str] = mapped_column(String(50), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SuggestedMeal(Base):
    __tablename__ = "suggested_meals"
    __table_args__ = (Index("ix_suggested_meals_user_date", "user_id", "date"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    menu_text: Mapped[str] = mapped_column(Text, nullable=False)
    ingredients: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Recipe(Base):
    """料理レシピマスタ（全ユーザー共通）。

    使用食品（ingredients）と作り方（instructions）をセットで保持する。
    - ingredients: [{name, quantity, unit}] → アレルゲン判定・買い物リスト集計に使用
    - instructions: 作り方手順 → 保護者向け表示に使用
    """

    __tablename__ = "recipes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    meal_type: Mapped[str] = mapped_column(String(20), nullable=False, default="main")  # main | side | soup | staple
    ingredients: Mapped[list] = mapped_column(JSON, default=list)
    instructions: Mapped[str] = mapped_column(Text, default="")
    cook_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    """ユーザーテスト・学祭アンケート用のフィードバック。

    アプリの使い勝手・改善要望を収集する。ログイン不要で投稿できる。
    """

    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 1〜5
    comment: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
