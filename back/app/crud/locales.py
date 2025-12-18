from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from pymongo.database import Database
from app.models.locales import LOCALES_COLLECTION

def build_query(*, status: Optional[str], codigo: Optional[str], pabellon: Optional[str],
                area_min: Optional[float], area_max: Optional[float],
                precio_min: Optional[int], precio_max: Optional[int]) -> Dict[str, Any]:
    query: Dict[str, Any] = {}
    if status:
        query["status"] = status
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

async def list_locales(db: Database[Any], *, query: Dict[str, Any], page: int, page_size: int) -> Tuple[List[dict], int]:
    col = db[LOCALES_COLLECTION]
    total = await col.count_documents(query)
    skip = (page - 1) * page_size
    cursor = col.find(query, {"_id": 0}).sort("codigo", 1).skip(skip).limit(page_size)
    items = [doc async for doc in cursor]
    return items, total

async def get_by_codigo(db: Database[Any], codigo: str) -> Optional[dict]:
    col = db[LOCALES_COLLECTION]
    return await col.find_one({"codigo": codigo}, {"_id": 0})
