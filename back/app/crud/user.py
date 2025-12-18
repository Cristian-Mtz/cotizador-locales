from __future__ import annotations

from typing import Any, List

from pymongo.database import Database

from app.models.user import USERS_COLLECTION


async def list_users(db: Database[Any]) -> List[dict]:
    cursor = db[USERS_COLLECTION].find({}, {"_id": 0}).limit(50)
    return [doc async for doc in cursor]
