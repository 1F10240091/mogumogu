"""Pydantic スキーマ定義。"""

import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

# パスワード強度チェック: 8文字以上・英字・数字を含む
_PASSWORD_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$")


def validate_password_strength(value: str) -> str:
    if not _PASSWORD_RE.match(value):
        raise ValueError("パスワードは8文字以上で、英字と数字をそれぞれ1文字以上含めてください")
    return value


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- 認証 ---
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    display_name: Optional[str] = None

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        return validate_password_strength(v)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(ORMModel):
    id: str
    email: EmailStr
    display_name: Optional[str] = None


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8)

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        return validate_password_strength(v)


# --- お子様 ---
class AllergyCreate(BaseModel):
    ingredient: str


class AllergyResponse(ORMModel):
    id: str
    ingredient: str


class PreferenceCreate(BaseModel):
    ingredient: str
    mode: str = "exclude"


class PreferenceResponse(ORMModel):
    id: str
    ingredient: str
    mode: str


class ChildCreate(BaseModel):
    name: str
    birth_date: Optional[date] = None
    allergies: list[AllergyCreate] = []
    preferences: list[PreferenceCreate] = []


class ChildUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None


class ChildResponse(ORMModel):
    id: str
    name: str
    birth_date: Optional[date] = None
    allergies: list[AllergyResponse] = []
    preferences: list[PreferenceResponse] = []


# --- 献立表（OCR） ---
class NurseryMenuCreate(BaseModel):
    date: date
    menu_text: str


class NurseryMenuResponse(ORMModel):
    id: str
    date: date
    menu_text: str
    ingredients: dict


# --- AI 献立提案 ---
class GenerateRequest(BaseModel):
    child_id: str
    menu_date: date
    days: int = Field(default=1, ge=1, le=7)


class MealResponse(ORMModel):
    id: str
    date: date
    menu_text: str
    ingredients: dict


class GenerateResponse(BaseModel):
    meals: list[MealResponse]


# --- レシピマスタ ---
class Ingredient(BaseModel):
    name: str
    quantity: str = ""
    unit: str = ""


class RecipeCreate(BaseModel):
    name: str
    meal_type: str = "main"
    ingredients: list[Ingredient] = []
    instructions: str = ""
    cook_time_minutes: int | None = Field(default=None, ge=1)


class RecipeUpdate(BaseModel):
    name: str | None = None
    meal_type: str | None = None
    ingredients: list[Ingredient] | None = None
    instructions: str | None = None
    cook_time_minutes: int | None = Field(default=None, ge=1)


class RecipeResponse(ORMModel):
    id: str
    name: str
    meal_type: str
    ingredients: list[Ingredient]
    instructions: str
    cook_time_minutes: int | None


class RecipeSearchResponse(BaseModel):
    recipes: list[RecipeResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
