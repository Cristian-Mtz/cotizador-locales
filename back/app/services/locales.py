from __future__ import annotations

from typing import Any, List, Optional, Tuple
from pymongo.database import Database
from app.crud.locales import build_query, get_by_codigo, list_locales
from app.errors import NotFound
from app.models.locales import STATUS_DISPONIBLE
from app.utils.normalize import normalize_codigo

async def search_locales(db: Database[Any], *, codigo: Optional[str], pabellon: Optional[str],
                         area_min: Optional[float], area_max: Optional[float],
                         precio_min: Optional[int], precio_max: Optional[int],
                         page: int, page_size: int) -> Tuple[List[dict], int]:
    codigo_norm = normalize_codigo(codigo) if codigo else None
    query = build_query(
        status=STATUS_DISPONIBLE,
        codigo=codigo_norm,
        pabellon=pabellon,
        area_min=area_min,
        area_max=area_max,
        precio_min=precio_min,
        precio_max=precio_max,
    )
    return await list_locales(db, query=query, page=page, page_size=page_size)

async def get_local_detail(db: Database[Any], codigo: str) -> dict:
    codigo_norm = normalize_codigo(codigo)
    doc = await get_by_codigo(db, codigo_norm)
    if doc is None:
        raise NotFound(code="LOCAL_NOT_FOUND", message=f"Local '{codigo_norm}' no existe.")
    return doc
