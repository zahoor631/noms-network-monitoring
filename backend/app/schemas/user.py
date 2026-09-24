from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str | None = None
    role: UserRole = UserRole.viewer


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None
    avatar_url: str | None = None


class UserOut(UserBase):
    id: int
    is_active: bool
    avatar_url: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True