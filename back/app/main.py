from __future__ import annotations

import json
import logging
import logging.config
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, List, Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pymongo import AsyncMongoClient

from app.routers.items import router as items_router
from app.routers.users import router as users_router
from app.routers.locales import router as locales_router
from app.routers.cotizaciones import router as cotizaciones_router

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="fastapi-mongo-starter", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    environment: Literal["local", "dev", "prod"] = Field(default="local", alias="ENVIRONMENT")
    api_v1_prefix: str = Field(default="/api", alias="API_V1_PREFIX")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:4200"], alias="CORS_ORIGINS")

    mongodb_uri: str = Field(default="mongodb://localhost:27017", alias="MONGODB_URI")
    mongodb_db: str = Field(default="app_db", alias="MONGODB_DB")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors(cls, v: Any) -> List[str]:
        if v is None:
            return ["http://localhost:4200"]
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return ["http://localhost:4200"]
            if s.startswith("["):
                try:
                    data = json.loads(s)
                    if isinstance(data, list):
                        return [str(x).strip() for x in data if str(x).strip()]
                except Exception:
                    pass
            return [i.strip() for i in s.split(",") if i.strip()]
        return ["http://localhost:4200"]


settings = Settings()


def _configure_logging() -> None:
    ini = Path("logging.ini")
    if ini.exists():
        logging.config.fileConfig(ini, disable_existing_loggers=False)
        logging.getLogger().setLevel(settings.log_level)
        return
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ! BetterComments: tolerant Mongo connection, API can still start without Mongo for /health
    client = AsyncMongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=2000)
    try:
        await client.aconnect()
        await client.admin.command("ping")
        app.state.mongo_client = client
        app.state.mongo_db = client[settings.mongodb_db]
        app.state.mongo_ready = True
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


_configure_logging()

app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["meta"])
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": f"{settings.api_v1_prefix}/health",
    }


@app.get(f"{settings.api_v1_prefix}/health", tags=["health"])
async def health():
    return {"status": "ok", "mongo_connected": bool(getattr(app.state, "mongo_ready", False))}


app.include_router(items_router, prefix=settings.api_v1_prefix)
app.include_router(users_router, prefix=settings.api_v1_prefix)
app.include_router(locales_router, prefix=settings.api_v1_prefix)
app.include_router(cotizaciones_router, prefix=settings.api_v1_prefix)
