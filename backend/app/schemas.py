from datetime import date, datetime
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    display_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class ChildBase(BaseModel):
    name: str
    birth_date: Optional[date] = None
    gender: Optional[str] = None


class ChildCreate(ChildBase):
    pass


class ChildUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None


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
    allergies: List[AllergyResponse] = []
    preferences: List[PreferenceResponse] = []