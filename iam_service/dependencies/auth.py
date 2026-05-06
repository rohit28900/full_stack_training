from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from core.config import settings
from schemas.auth_schema import TokenPayload


# Swagger will use this for "Authorize" button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Get current user from JWT
def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return TokenPayload(**payload)

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")