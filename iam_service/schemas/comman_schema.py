from pydantic import BaseModel


class MessageResponse(BaseModel):
    data: str