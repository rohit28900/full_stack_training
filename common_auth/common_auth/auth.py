from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security = HTTPBearer()


def get_current_user(settings):
    """
    Factory function → inject settings from each service
    """

    def dependency(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        try:
            token = credentials.credentials

            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )

            return payload

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

    return dependency