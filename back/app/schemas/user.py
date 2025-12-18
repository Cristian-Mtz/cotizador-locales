from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: str = Field(..., description="User identifier")
    email: EmailStr
    name: str
