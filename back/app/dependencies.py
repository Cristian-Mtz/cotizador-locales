from __future__ import annotations

from typing import Any

from fastapi import Request
from pymongo.database import Database

from app.utils.validation import ensure_mongo_ready


def get_db(request: Request) -> Database[Any]:
    """Dependency: returns Mongo Database if ready, otherwise raises 503."""
    ensure_mongo_ready(request)
    return request.app.state.mongo_db
