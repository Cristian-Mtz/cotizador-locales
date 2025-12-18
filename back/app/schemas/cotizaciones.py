from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CotizacionCreate(BaseModel):
    prospecto_email: EmailStr
    local_codigo: str = Field(..., min_length=1)
    duracion_meses: int = Field(..., ge=1)
    notas: Optional[str] = None


class CotizacionOut(BaseModel):
    id: str
    prospecto_email: EmailStr
    local_codigo: str
    duracion_meses: int
    notas: Optional[str] = None
    subtotal: int
    iva: int
    total: int
    created_at: datetime
