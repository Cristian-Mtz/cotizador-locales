from __future__ import annotations
from fastapi import APIRouter, Request
router = APIRouter(tags=["health"])

@router.get("/health")
async def health(request: Request):
    return {"status": "ok", "mongo_connected": bool(getattr(request.app.state, "mongo_ready", False))}
