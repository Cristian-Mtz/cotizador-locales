from __future__ import annotations
from typing import Any, Optional
from fastapi import APIRouter, Depends, Path, Query
from pymongo.database import Database
from app.dependencies import get_db
from app.schemas.errors import ErrorResponse
from app.schemas.locales import LocalOut, LocalesListResponse
from app.services.locales import get_local_detail, search_locales
from app.utils.pagination import total_pages

router = APIRouter(prefix="/locales", tags=["locales"])

@router.get("", response_model=LocalesListResponse)
async def list_locales_endpoint(
    codigo: Optional[str] = Query(default=None),
    pabellon: Optional[str] = Query(default=None),
    area_min: Optional[float] = Query(default=None, ge=0),
    area_max: Optional[float] = Query(default=None, ge=0),
    precio_min: Optional[int] = Query(default=None, ge=0),
    precio_max: Optional[int] = Query(default=None, ge=0),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    db: Database[Any] = Depends(get_db),
) -> LocalesListResponse:
    items, total = await search_locales(
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
    return LocalesListResponse(items=items, page=page, page_size=page_size, total=total, total_pages=total_pages(total, page_size))

@router.get("/{codigo}", response_model=LocalOut, responses={404: {"model": ErrorResponse}})
async def get_local_endpoint(
    codigo: str = Path(...),
    db: Database[Any] = Depends(get_db),
) -> LocalOut:
    return await get_local_detail(db, codigo=codigo)
