from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TicketCreate(BaseModel):
    title: str = Field(min_length=5, max_length=120)
    description: str = Field(min_length=10, max_length=2000)
    priority: Literal["low", "medium", "high"] = "medium"


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    priority: Literal["low", "medium", "high"]


class TicketCreatedResponse(BaseModel):
    message: str
    data: TicketResponse


class TicketDeletedResponse(BaseModel):
    message: str
    id: int
