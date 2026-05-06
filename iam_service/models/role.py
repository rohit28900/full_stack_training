from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, nullable=False)