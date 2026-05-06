from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.database import get_session
from schemas.auth_schema import LoginRequest, TokenResponse
from service.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
service = AuthService()


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_session)):
    try:
        user = service.authenticate(db, data.email, data.password)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        payload = service.build_payload(db, user)
        token = service.create_token(payload)

        return {"access_token": token}

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(status_code=500, detail="Login failed")