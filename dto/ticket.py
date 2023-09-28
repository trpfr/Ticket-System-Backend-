#  DTO file is used to define the data model for the API.
from typing import Optional

from pydantic import BaseModel, Field


class Ticket(BaseModel):
    id: str
    title: str
    content: str
    userEmail: str
    creationTime: int
    labels: list
    user_id: Optional[str]

    class Config:
        orm_mode = True
