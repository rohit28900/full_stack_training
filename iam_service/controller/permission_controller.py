from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.permission_schema import (
    PermissionCreate, PermissionResponse
)
from service.permission_service import PermissionService

router = APIRouter(prefix="/permissions", tags=["Permissions"])
service = PermissionService()


@router.post("/", response_model=PermissionResponse)
def create_permission(data: PermissionCreate, db: Session = Depends(get_session)):
    try:
        return service.create_permission(db, data)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create permission")


@router.get("/", response_model=list[PermissionResponse])
def get_permissions(db: Session = Depends(get_session)):
    try:
        return service.get_all_permissions(db)

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch permissions")