from datetime import date, datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RecipeCategory(str, Enum):
    MAIN_DISH = "main_dish"
    SIDE_DISH = "side_dish"
    SOUP = "soup"
    RICE = "rice"
    NOODLE = "noodle"
    DESSERT = "dessert"
    OTHER = "other"


class UserBase(BaseModel):
    email: EmailStr
    display_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    display_name: str | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class ChildBase(BaseModel):
    name: str
    birth_date: date | None = None
    gender: str | None = None


class ChildCreate(ChildBase):
    pass


class ChildUpdate(BaseModel):
    name: str | None = None
    birth_date: date | None = None
    gender: str | None = None


class ChildResponse(ChildBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    created_at: datetime


class AllergyBase(BaseModel):
    ingredient: str


class AllergyCreate(AllergyBase):
    pass


class AllergyResponse(AllergyBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    child_id: UUID


class PreferenceBase(BaseModel):
    ingredient: str
    mode: str  # exclude / improve


class PreferenceCreate(PreferenceBase):
    pass


class PreferenceResponse(PreferenceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    child_id: UUID


class ChildWithDetails(ChildResponse):
    allergies: list[AllergyResponse] = []
    preferences: list[PreferenceResponse] = []


class RecipeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    category: RecipeCategory
    ingredients: list[str] = Field(..., min_length=1)
    instructions: list[str] = Field(..., min_length=1)
    cooking_time_minutes: int | None = Field(None, gt=0, le=10080)
    servings: int | None = Field(None, ge=1, le=100)
    image_url: str | None = None
    source_url: str | None = None
    tags: list[str] = []


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: RecipeCategory | None = None
    ingredients: list[str] | None = None
    instructions: list[str] | None = None
    cooking_time_minutes: int | None = None
    servings: int | None = None
    image_url: str | None = None
    source_url: str | None = None
    tags: list[str] | None = None
    is_public: bool | None = None


class RecipeResponse(RecipeBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    is_public: bool


class RecipeSearchParams(BaseModel):
    keyword: str | None = None
    category: RecipeCategory | None = None
    ingredients: list[str] | None = None
    tags: list[str] | None = None
    max_cooking_time: int | None = None
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)


class RecipeSearchResponse(BaseModel):
    recipes: list[RecipeResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
