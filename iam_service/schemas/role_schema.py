from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# ---------- Create / Update ----------

class RoleCreate(BaseModel):
    name: str


class RoleUpdate(BaseModel):
    name: Optional[str] = None


# ---------- Response ----------

class RoleResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


# ---------- Permission Assignment ----------

class AssignPermissionToRole(BaseModel):
    role_id: UUID
    permission_id: UUID


class RemovePermissionFromRole(BaseModel):
    role_id: UUID
    permission_id: UUID