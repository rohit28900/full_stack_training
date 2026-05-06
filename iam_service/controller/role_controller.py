from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID

from core.database import get_session
from schemas.role_schema import (
    RoleCreate, RoleResponse
)
from service.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["Roles"])
service = RoleService()


@router.post("/", response_model=RoleResponse)
def create_role(data: RoleCreate, db: Session = Depends(get_session)):
    try:
        return service.create_role(db, data)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create role")
    
@router.post("/assign-permission")
def assign_permission_to_role(
    role_id: UUID,
    permission_id: UUID,
    db: Session = Depends(get_session)
):
    try:
        return service.assign_permission_to_role(db, role_id, permission_id)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to assign permission")


@router.get("/", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_session)):
    try:
        return service.get_all_roles(db)

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch roles")