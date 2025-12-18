from __future__ import annotations

from typing import Any, List

from pymongo.database import Database

from app.models.item import ITEMS_COLLECTION


async def list_items(db: Database[Any]) -> List[dict]:
    cursor = db[ITEMS_COLLECTION].find({}, {"_id": 0}).limit(50)
    return [doc async for doc in cursor]
