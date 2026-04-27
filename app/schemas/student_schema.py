from pydantic import BaseModel, EmailStr
from typing import Optional


class StudentBase(BaseModel):
    name: str
    email: str
    age: Optional[int] = None


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True