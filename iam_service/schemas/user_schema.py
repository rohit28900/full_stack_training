from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional


# ---------- Create / Update ----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


# ---------- Response ----------

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Role Assignment ----------

class AssignRoleToUser(BaseModel):
    user_id: UUID
    role_id: UUID


class RemoveRoleFromUser(BaseModel):
    user_id: UUID
    role_id: UUID