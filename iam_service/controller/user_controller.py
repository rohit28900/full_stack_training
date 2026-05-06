from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from uuid import UUID

from core.database import get_session
from schemas.user_schema import (
    UserCreate,
    UserResponse,
    AssignRoleToUser 
)
from service.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])
service = UserService()


# Create User
@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_session)):
    try:
        return service.create_user(db, data)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create user")


# Get User by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_session)):
    try:
        user = service.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch user")


# Get All Users
@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_session)):
    try:
        return service.get_all_users(db)

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch users")


#Delete User
@router.delete("/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_session)):
    try:
        success = service.delete_user(db, user_id)

        if not success:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User deleted successfully"}

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete user")
    
@router.post("/assign-role")
def assign_role_to_user(
    data: AssignRoleToUser,
    db: Session = Depends(get_session)
):
    try:
        return service.assign_role_to_user(db, data.user_id, data.role_id)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to assign role")