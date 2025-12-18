from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional
from pymongo.database import Database
from app.crud.cotizaciones import insert_cotizacion, list_by_email
from app.crud.locales import get_by_codigo
from app.errors import Conflict, NotFound
from app.models.cotizaciones import IVA_RATE
from app.models.locales import STATUS_DISPONIBLE
from app.utils.mongo import mongo_to_out
from app.utils.normalize import normalize_codigo, normalize_email

def _calc_iva_total(subtotal: int) -> tuple[int, int]:
    iva = int((Decimal(subtotal) * Decimal(str(IVA_RATE))).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    return iva, subtotal + iva

async def create_cotizacion(db: Database[Any], *, prospecto_email: str, local_codigo: str,
                            duracion_meses: int, notas: Optional[str]) -> Dict[str, Any]:
    email = normalize_email(prospecto_email)
    codigo = normalize_codigo(local_codigo)

    local = await get_by_codigo(db, codigo)
    if local is None:
        raise NotFound(code="LOCAL_NOT_FOUND", message=f"Local '{codigo}' no existe.")
    if local.get("status") != STATUS_DISPONIBLE:
        raise Conflict(code="LOCAL_NOT_AVAILABLE", message=f"Local '{codigo}' no está disponible para cotizar.")

    precio_mensual = int(local["precio_mensual"])
    subtotal = int(precio_mensual * duracion_meses)
    iva, total = _calc_iva_total(subtotal)
    created_at = datetime.now(timezone.utc)

    doc = {
        "prospecto_email": email,
        "local_codigo": codigo,
        "duracion_meses": duracion_meses,
        "notas": notas,
        "subtotal": subtotal,
        "iva": iva,
        "total": total,
        "created_at": created_at,
    }
    inserted_id = await insert_cotizacion(db, doc)
    return mongo_to_out({"_id": inserted_id, **doc})

async def get_cotizaciones_by_email(db: Database[Any], email: str) -> List[dict]:
    normalized = normalize_email(email)
    docs = await list_by_email(db, normalized)
    return [mongo_to_out(doc) for doc in docs]
