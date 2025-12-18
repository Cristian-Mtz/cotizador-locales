from __future__ import annotations

from typing import Any, List

from fastapi import APIRouter, Depends
from pymongo.database import Database

from app.crud.item import list_items
from app.dependencies import get_db

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=List[dict])
async def get_items(db: Database[Any] = Depends(get_db)) -> List[dict]:
    """List items (starter endpoint)."""
    return await list_items(db)
