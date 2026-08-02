import uuid
from datetime import date, datetime
from enum import Enum as PyEnum

from sqlalchemy import Enum, ForeignKey, MetaData, String, Text, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


def new_uuid() -> uuid.UUID:
    return uuid.uuid4()


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=naming_convention)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String)

    children: Mapped[list["Child"]] = relationship(
        "Child", back_populates="user", cascade="all, delete-orphan"
    )


class Child(Base, TimestampMixin):
    __tablename__ = "children"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String)
    birth_date: Mapped[date | None] = mapped_column()
    gender: Mapped[str | None] = mapped_column(String)

    user: Mapped["User"] = relationship("User", back_populates="children")
    allergies: Mapped[list["Allergy"]] = relationship(
        "Allergy", back_populates="child", cascade="all, delete-orphan"
    )
    preferences: Mapped[list["Preference"]] = relationship(
        "Preference", back_populates="child", cascade="all, delete-orphan"
    )


class Allergy(Base):
    __tablename__ = "allergies"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    child_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("children.id", ondelete="CASCADE"), index=True
    )
    ingredient: Mapped[str] = mapped_column(String)

    child: Mapped["Child"] = relationship("Child", back_populates="allergies")


class Preference(Base):
    __tablename__ = "preferences"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    child_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("children.id", ondelete="CASCADE"), index=True
    )
    ingredient: Mapped[str] = mapped_column(String)
    mode: Mapped[str] = mapped_column(String)  # exclude / improve

    child: Mapped["Child"] = relationship("Child", back_populates="preferences")


class RecipeCategory(str, PyEnum):
    MAIN_DISH = "main_dish"
    SIDE_DISH = "side_dish"
    SOUP = "soup"
    RICE = "rice"
    NOODLE = "noodle"
    DESSERT = "dessert"
    OTHER = "other"


class Recipe(Base, TimestampMixin):
    __tablename__ = "recipes"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[RecipeCategory] = mapped_column(Enum(RecipeCategory), index=True)
    ingredients: Mapped[str] = mapped_column(Text)  # JSON string
    instructions: Mapped[str] = mapped_column(Text)
    cooking_time_minutes: Mapped[str | None] = mapped_column(String)
    servings: Mapped[str | None] = mapped_column(String)
    image_url: Mapped[str | None] = mapped_column(String)
    source_url: Mapped[str | None] = mapped_column(String)
    tags: Mapped[str | None] = mapped_column(Text)  # JSON string array
    is_public: Mapped[str] = mapped_column(String, default="true")
