from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from pymongo import ASCENDING, DESCENDING, AsyncMongoClient
from pymongo.database import Database

from app.config import settings
from app.errors import ServiceUnavailable

logger = logging.getLogger(__name__)


async def _ensure_indexes(db: Database[Any]) -> None:
    await db["locales"].create_index([("codigo", ASCENDING)], unique=True, name="ux_locales_codigo")
    await db["locales"].create_index([("status", ASCENDING)], name="ix_locales_status")
    await db["locales"].create_index([("pabellon", ASCENDING)], name="ix_locales_pabellon")
    await db["locales"].create_index([("area_m2", ASCENDING)], name="ix_locales_area_m2")
    await db["locales"].create_index([("precio_mensual", ASCENDING)], name="ix_locales_precio_mensual")

    await db["cotizaciones"].create_index(
        [("prospecto_email", ASCENDING), ("created_at", DESCENDING)],
        name="ix_cotizaciones_email_created_at",
    )
    await db["cotizaciones"].create_index([("local_codigo", ASCENDING)], name="ix_cotizaciones_local_codigo")


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncMongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=2000)
    try:
        await client.aconnect()
        await client.admin.command("ping")

        db = client[settings.mongodb_db]
        app.state.mongo_client = client
        app.state.mongo_db = db
        app.state.mongo_ready = True

        await _ensure_indexes(db)

        logger.info("Mongo connected (%s / %s)", settings.mongodb_uri, settings.mongodb_db)
    except Exception as e:
        app.state.mongo_client = None
        app.state.mongo_db = None
        app.state.mongo_ready = False
        logger.warning("Mongo NOT connected (%s): %s", settings.mongodb_uri, e)

    yield

    if getattr(app.state, "mongo_client", None) is not None:
        app.state.mongo_client.close()
        logger.info("Mongo connection closed")


def get_db(request: Request) -> Database[Any]:
    db = getattr(request.app.state, "mongo_db", None)
    if db is None or not bool(getattr(request.app.state, "mongo_ready", False)):
        raise ServiceUnavailable(code="MONGO_NOT_READY", message="MongoDB connection is not ready. Is Mongo running on localhost:27017?")
    return db
