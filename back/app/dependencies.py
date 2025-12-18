from __future__ import annotations
from typing import Any
from fastapi import Request
from pymongo.database import Database
from app.db import get_db as _get_db

def get_db(request: Request) -> Database[Any]:
    return _get_db(request)
