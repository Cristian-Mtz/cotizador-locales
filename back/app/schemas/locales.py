from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field

class Ubicacion(BaseModel):
    lat: float
    lng: float

class Caracteristicas(BaseModel):
    instalacion_electrica: str
    carga_maxima_kg: int
    altura_m: float

class LocalOut(BaseModel):
    codigo: str
    pabellon: str
    area_m2: float
    precio_mensual: int
    status: str
    ubicacion: Ubicacion
    caracteristicas: Caracteristicas

class LocalesListResponse(BaseModel):
    items: List[LocalOut]
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1, le=50)
    total: int = Field(..., ge=0)
    total_pages: int = Field(..., ge=0)
