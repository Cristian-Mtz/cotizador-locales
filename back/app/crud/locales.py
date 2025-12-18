from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from pymongo.database import Database

from app.models.locales import LOCALES_COLLECTION, STATUS_DISPONIBLE


def build_locales_query(
    *,
    codigo: Optional[str],
    pabellon: Optional[str],
    area_min: Optional[float],
    area_max: Optional[float],
    precio_min: Optional[int],
    precio_max: Optional[int],
) -> Dict[str, Any]:
    # ! BetterComments: el enunciado pide "locales disponibles", así que forzamos status=disponible
    query: Dict[str, Any] = {"status": STATUS_DISPONIBLE}

    if codigo:
        query["codigo"] = codigo

    if pabellon:
        query["pabellon"] = pabellon

    if area_min is not None or area_max is not None:
        query["area_m2"] = {}
        if area_min is not None:
            query["area_m2"]["$gte"] = area_min
        if area_max is not None:
            query["area_m2"]["$lte"] = area_max

    if precio_min is not None or precio_max is not None:
        query["precio_mensual"] = {}
        if precio_min is not None:
            query["precio_mensual"]["$gte"] = precio_min
        if precio_max is not None:
            query["precio_mensual"]["$lte"] = precio_max

    return query


async def list_locales(
    db: Database[Any],
    *,
    codigo: Optional[str],
    pabellon: Optional[str],
    area_min: Optional[float],
    area_max: Optional[float],
    precio_min: Optional[int],
    precio_max: Optional[int],
    page: int,
    page_size: int,
) -> Tuple[List[dict], int]:
    query = build_locales_query(
        codigo=codigo,
        pabellon=pabellon,
        area_min=area_min,
        area_max=area_max,
        precio_min=precio_min,
        precio_max=precio_max,
    )

    collection = db[LOCALES_COLLECTION]

    total = await collection.count_documents(query)

    skip = (page - 1) * page_size

    cursor = (
        collection.find(query, {"_id": 0})
        .sort("codigo", 1)
        .skip(skip)
        .limit(page_size)
    )

    items = [doc async for doc in cursor]
    return items, total
