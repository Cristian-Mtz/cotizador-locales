from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List

from bson import ObjectId
from pymongo.database import Database

from app.models.cotizaciones import COTIZACIONES_COLLECTION, IVA_RATE
from app.models.locales import LOCALES_COLLECTION, STATUS_DISPONIBLE

async def list_cotizaciones_by_email(db: Database[Any], email: str) -> List[dict]:
    normalized = email.lower().strip()

    cursor = (
        db[COTIZACIONES_COLLECTION]
        .find({"prospecto_email": normalized})
        .sort("created_at", -1)
        .limit(200)
    )

    items: List[dict] = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        items.append(doc)

    return items


async def create_cotizacion(
    db: Database[Any],
    *,
    prospecto_email: str,
    local_codigo: str,
    duracion_meses: int,
    notas: str | None,
) -> Dict[str, Any]:
    # 1) validar local existe
    local = await db[LOCALES_COLLECTION].find_one({"codigo": local_codigo}, {"_id": 0})
    if local is None:
        return {
            "error": {"code": "LOCAL_NOT_FOUND", "message": f"Local '{local_codigo}' no existe."},
            "status_code": 404,
        }

    # 2) validar disponible: el flujo del sistema es “buscar disponibles y cotizar”
    if local.get("status") != STATUS_DISPONIBLE:
        return {
            "error": {
                "code": "LOCAL_NOT_AVAILABLE",
                "message": f"Local '{local_codigo}' no está disponible para cotizar.",
            },
            "status_code": 409,
        }

    precio_mensual = int(local["precio_mensual"])

    # 3) cálculos (IVA 16%)
    subtotal = int(precio_mensual * duracion_meses)
    iva = int(
        (Decimal(subtotal) * Decimal(str(IVA_RATE))).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    )
    total = int(subtotal + iva)

    created_at = datetime.now(timezone.utc)

    doc = {
        "prospecto_email": prospecto_email.lower().strip(),
        "local_codigo": local_codigo,
        "duracion_meses": duracion_meses,
        "notas": notas,
        "subtotal": subtotal,
        "iva": iva,
        "total": total,
        "created_at": created_at,
    }

    res = await db[COTIZACIONES_COLLECTION].insert_one(doc)

    return {"id": str(res.inserted_id), **doc}
