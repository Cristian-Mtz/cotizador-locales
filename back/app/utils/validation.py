from __future__ import annotations

from fastapi import HTTPException, Request


def ensure_mongo_ready(request: Request) -> None:
    """Raises 503 if MongoDB is not connected."""
    if not bool(getattr(request.app.state, "mongo_ready", False)):
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "code": "MONGO_NOT_READY",
                    "message": "MongoDB connection is not ready. Is Mongo running on localhost:27017?",
                }
            },
        )
