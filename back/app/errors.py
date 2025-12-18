from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@dataclass(frozen=True)
class AppError(Exception):
    code: str
    message: str
    status_code: int = 400
    details: Optional[Any] = None


class NotFound(AppError):
    def __init__(self, code: str, message: str, details: Optional[Any] = None) -> None:
        super().__init__(code=code, message=message, status_code=404, details=details)


class Conflict(AppError):
    def __init__(self, code: str, message: str, details: Optional[Any] = None) -> None:
        super().__init__(code=code, message=message, status_code=409, details=details)


class ServiceUnavailable(AppError):
    def __init__(self, code: str, message: str, details: Optional[Any] = None) -> None:
        super().__init__(code=code, message=message, status_code=503, details=details)


def _payload(code: str, message: str, details: Optional[Any] = None) -> dict:
    body = {"code": code, "message": message}
    if details is not None:
        body["details"] = details
    return {"error": body}


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=_payload(exc.code, exc.message, exc.details))


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=_payload("HTTP_ERROR", str(exc.detail)))


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content=_payload("VALIDATION_ERROR", "Request validation failed", details=exc.errors()))
