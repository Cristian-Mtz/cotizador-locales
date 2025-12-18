from __future__ import annotations

from typing import Any, List

from fastapi import APIRouter, Depends
from pymongo.database import Database

from app.crud.user import list_users
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[dict])
async def get_users(db: Database[Any] = Depends(get_db)) -> List[dict]:
    """List users (starter endpoint)."""
    return await list_users(db)
