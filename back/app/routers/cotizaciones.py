from __future__ import annotations

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Path
from pymongo.database import Database

from app.crud.cotizaciones import create_cotizacion, list_cotizaciones_by_email
from app.dependencies import get_db
from app.schemas.cotizaciones import CotizacionCreate, CotizacionOut

router = APIRouter(prefix="/cotizaciones", tags=["cotizaciones"])


@router.get("/prospecto/{email}", response_model=List[CotizacionOut])
async def get_cotizaciones_prospecto(
    email: str = Path(..., description="Email del prospecto"),
    db: Database[Any] = Depends(get_db),
) -> List[dict]:
    return await list_cotizaciones_by_email(db, email=email)


@router.post("", response_model=CotizacionOut, status_code=status.HTTP_201_CREATED)
async def post_cotizacion(
    payload: CotizacionCreate,
    db: Database[Any] = Depends(get_db),
) -> CotizacionOut:
    result = await create_cotizacion(
        db,
        prospecto_email=str(payload.prospecto_email),
        local_codigo=payload.local_codigo,
        duracion_meses=payload.duracion_meses,
        notas=payload.notas,
    )

    # Si CRUD devolvió error controlado
    if "status_code" in result:
        raise HTTPException(status_code=result["status_code"], detail={"error": result["error"]})

    return result  # type: ignore[return-value]
