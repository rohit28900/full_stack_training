from pydantic import BaseModel, EmailStr
from typing import List


# ---------- Auth Requests ----------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------- Token ----------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    roles: List[str] = []
    permissions: List[str] = []