from __future__ import annotations
from typing import Any, List
from fastapi import APIRouter, Depends, Path, status
from pymongo.database import Database
from app.dependencies import get_db
from app.schemas.cotizaciones import CotizacionCreate, CotizacionOut
from app.schemas.errors import ErrorResponse
from app.services.cotizaciones import create_cotizacion, get_cotizaciones_by_email

router = APIRouter(prefix="/cotizaciones", tags=["cotizaciones"])

@router.post("", response_model=CotizacionOut, status_code=status.HTTP_201_CREATED, responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}})
async def post_cotizacion_endpoint(payload: CotizacionCreate, db: Database[Any] = Depends(get_db)) -> CotizacionOut:
    return await create_cotizacion(db, prospecto_email=str(payload.prospecto_email), local_codigo=payload.local_codigo, duracion_meses=payload.duracion_meses, notas=payload.notas)

@router.get("/prospecto/{email}", response_model=List[CotizacionOut])
async def list_cotizaciones_prospecto_endpoint(email: str = Path(...), db: Database[Any] = Depends(get_db)) -> List[dict]:
    return await get_cotizaciones_by_email(db, email=email)
