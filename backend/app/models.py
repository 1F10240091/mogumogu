import uuid

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    MetaData,
    String,
    Uuid,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func

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
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=new_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    display_name = Column(String, nullable=False)

    children = relationship(
        "Child", back_populates="user", cascade="all, delete-orphan"
    )


class Child(Base, TimestampMixin):
    __tablename__ = "children"

    id = Column(Uuid, primary_key=True, default=new_uuid)
    user_id = Column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    gender = Column(String, nullable=True)

    user = relationship("User", back_populates="children")
    allergies = relationship(
        "Allergy", back_populates="child", cascade="all, delete-orphan"
    )
    preferences = relationship(
        "Preference", back_populates="child", cascade="all, delete-orphan"
    )


class Allergy(Base):
    __tablename__ = "allergies"

    id = Column(Uuid, primary_key=True, default=new_uuid)
    child_id = Column(
        Uuid, ForeignKey("children.id", ondelete="CASCADE"), nullable=False, index=True
    )
    ingredient = Column(String, nullable=False)

    child = relationship("Child", back_populates="allergies")


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Uuid, primary_key=True, default=new_uuid)
    child_id = Column(
        Uuid, ForeignKey("children.id", ondelete="CASCADE"), nullable=False, index=True
    )
    ingredient = Column(String, nullable=False)
    mode = Column(String, nullable=False)  # exclude / improve

    child = relationship("Child", back_populates="preferences")
