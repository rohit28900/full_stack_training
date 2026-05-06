from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# ---------- Create / Update ----------

class PermissionCreate(BaseModel):
    name: str


class PermissionUpdate(BaseModel):
    name: Optional[str] = None


# ---------- Response ----------

class PermissionResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True