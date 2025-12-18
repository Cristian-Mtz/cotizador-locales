from __future__ import annotations

import logging
import logging.config
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.db import lifespan
from app.errors import AppError, app_error_handler, http_exception_handler, validation_exception_handler
from app.routers.cotizaciones import router as cotizaciones_router
from app.routers.health import router as health_router
from app.routers.locales import router as locales_router

logger = logging.getLogger(__name__)

def _configure_logging() -> None:
    ini = Path("logging.ini")
    if ini.exists():
        logging.config.fileConfig(ini, disable_existing_loggers=False)
        logging.getLogger().setLevel(settings.log_level)
    else:
        logging.basicConfig(level=settings.log_level, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

def create_app() -> FastAPI:
    _configure_logging()
    app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    @app.get("/", tags=["meta"])
    async def root():
        return {"name": settings.app_name, "version": settings.app_version, "docs": "/docs", "health": f"{settings.api_v1_prefix}/health"}

    app.include_router(health_router, prefix=settings.api_v1_prefix)
    app.include_router(locales_router, prefix=settings.api_v1_prefix)
    app.include_router(cotizaciones_router, prefix=settings.api_v1_prefix)

    return app

app = create_app()
