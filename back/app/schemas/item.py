from __future__ import annotations

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: str = Field(..., description="Item identifier")
    name: str
