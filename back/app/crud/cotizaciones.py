from __future__ import annotations

from typing import Any, Dict, List
from bson import ObjectId
from pymongo.database import Database
from app.models.cotizaciones import COTIZACIONES_COLLECTION

async def insert_cotizacion(db: Database[Any], doc: Dict[str, Any]) -> ObjectId:
    res = await db[COTIZACIONES_COLLECTION].insert_one(doc)
    return res.inserted_id

async def list_by_email(db: Database[Any], email: str) -> List[dict]:
    cursor = db[COTIZACIONES_COLLECTION].find({"prospecto_email": email}).sort("created_at", -1).limit(200)
    return [doc async for doc in cursor]
