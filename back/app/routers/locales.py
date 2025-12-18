from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, Query
from pymongo.database import Database

from app.crud.locales import list_locales
from app.dependencies import get_db
from app.schemas.locales import LocalesListResponse
from app.utils.pagination import total_pages

router = APIRouter(prefix="/locales", tags=["locales"])


@router.get("", response_model=LocalesListResponse)
async def get_locales(
    codigo: Optional[str] = Query(default=None, description="Código exacto del local"),
    pabellon: Optional[str] = Query(default=None, description="Pabellón (ej: A, B, C)"),
    area_min: Optional[float] = Query(default=None, ge=0, description="Área mínima (m2)"),
    area_max: Optional[float] = Query(default=None, ge=0, description="Área máxima (m2)"),
    precio_min: Optional[int] = Query(default=None, ge=0, description="Precio mínimo mensual"),
    precio_max: Optional[int] = Query(default=None, ge=0, description="Precio máximo mensual"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    db: Database[Any] = Depends(get_db),
) -> LocalesListResponse:
    items, total = await list_locales(
        db,
        codigo=codigo,
        pabellon=pabellon,
        area_min=area_min,
        area_max=area_max,
        precio_min=precio_min,
        precio_max=precio_max,
        page=page,
        page_size=page_size,
    )

    return LocalesListResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages(total, page_size),
    )
