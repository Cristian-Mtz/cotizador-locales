from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict

def locale_doc(**overrides: Any) -> Dict[str, Any]:
    base = {
        "codigo": "L-A-001",
        "pabellon": "A",
        "area_m2": 45.5,
        "precio_mensual": 15000,
        "status": "disponible",
        "ubicacion": {"lat": 19.4326, "lng": -99.1332},
        "caracteristicas": {"instalacion_electrica": "220V", "carga_maxima_kg": 500, "altura_m": 3.5},
    }
    base.update(overrides)
    return base

def cotizacion_doc(**overrides: Any) -> Dict[str, Any]:
    base = {
        "prospecto_email": "demo@mail.com",
        "local_codigo": "L-A-001",
        "duracion_meses": 6,
        "notas": "Prueba",
        "subtotal": 90000,
        "iva": 14400,
        "total": 104400,
        "created_at": datetime.now(timezone.utc),
    }
    base.update(overrides)
    return base
