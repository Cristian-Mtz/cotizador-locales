from __future__ import annotations

import argparse
import asyncio
from typing import List

from pymongo import ASCENDING, AsyncMongoClient

from app.main import settings
from app.models.locales import (
    LOCALES_COLLECTION,
    STATUS_DISPONIBLE,
    STATUS_MANTENIMIENTO,
    STATUS_OCUPADO,
)


def seed_data() -> List[dict]:
    # Estructura (codigo, pabellon, area_m2, precio_mensual, status, ubicacion, caracteristicas)
    return [
        {
            "codigo": "L-A-001",
            "pabellon": "A",
            "area_m2": 45.5,
            "precio_mensual": 15000,
            "status": STATUS_DISPONIBLE,
            "ubicacion": {"lat": 19.4326, "lng": -99.1332},
            "caracteristicas": {"instalacion_electrica": "220V", "carga_maxima_kg": 500, "altura_m": 3.5},
        },
        {
            "codigo": "L-A-002",
            "pabellon": "A",
            "area_m2": 30.0,
            "precio_mensual": 12000,
            "status": STATUS_DISPONIBLE,
            "ubicacion": {"lat": 19.4332, "lng": -99.1340},
            "caracteristicas": {"instalacion_electrica": "110V", "carga_maxima_kg": 300, "altura_m": 3.0},
        },
        {
            "codigo": "L-A-003",
            "pabellon": "A",
            "area_m2": 60.0,
            "precio_mensual": 22000,
            "status": STATUS_OCUPADO,
            "ubicacion": {"lat": 19.4317, "lng": -99.1324},
            "caracteristicas": {"instalacion_electrica": "220V", "carga_maxima_kg": 700, "altura_m": 4.0},
        },
        {
            "codigo": "L-A-004",
            "pabellon": "A",
            "area_m2": 40.0,
            "precio_mensual": 14000,
            "status": STATUS_DISPONIBLE,
            "ubicacion": {"lat": 19.4309, "lng": -99.1318},
            "caracteristicas": {"instalacion_electrica": "220V", "carga_maxima_kg": 450, "altura_m": 3.2},
        },
        {
            "codigo": "L-B-001",
            "pabellon": "B",
            "area_m2": 80.0,
            "precio_mensual": 30000,
            "status": STATUS_DISPONIBLE,
            "ubicacion": {"lat": 19.4341, "lng": -99.1352},
            "caracteristicas": {"instalacion_electrica": "440V", "carga_maxima_kg": 1200, "altura_m": 5.0},
        },
        {
            "codigo": "L-B-002",
            "pabellon": "B",
            "area_m2": 55.0,
            "precio_mensual": 20000,
            "status": STATUS_MANTENIMIENTO,
            "ubicacion": {"lat": 19.4348, "lng": -99.1361},
            "caracteristicas": {"instalacion_electrica": "220V", "carga_maxima_kg": 650, "altura_m": 3.8},
        },
        {
            "codigo": "L-B-003",
            "pabellon": "B",
            "area_m2": 25.0,
            "precio_mensual": 9000,
            "status": STATUS_DISPONIBLE,
            "ubicacion": {"lat": 19.4354, "lng": -99.1344},
            "caracteristicas": {"instalacion_electrica": "110V", "carga_maxima_kg": 250, "altura_m": 2.8},
        },
        {
            "codigo": "L-C-001",
            "pabellon": "C",
            "area_m2": 35.0,
            "precio_mensual": 13000,
            "status": STATUS_DISPONIBLE,
            "ubicacion": {"lat": 19.4361, "lng": -99.1337},
            "caracteristicas": {"instalacion_electrica": "220V", "carga_maxima_kg": 400, "altura_m": 3.1},
        },
        {
            "codigo": "L-C-002",
            "pabellon": "C",
            "area_m2": 95.0,
            "precio_mensual": 38000,
            "status": STATUS_OCUPADO,
            "ubicacion": {"lat": 19.4370, "lng": -99.1329},
            "caracteristicas": {"instalacion_electrica": "440V", "carga_maxima_kg": 1500, "altura_m": 5.5},
        },
        {
            "codigo": "L-C-003",
            "pabellon": "C",
            "area_m2": 48.0,
            "precio_mensual": 17000,
            "status": STATUS_DISPONIBLE,
            "ubicacion": {"lat": 19.4376, "lng": -99.1319},
            "caracteristicas": {"instalacion_electrica": "220V", "carga_maxima_kg": 520, "altura_m": 3.6},
        },
    ]


async def ensure_indexes(col) -> None:
    # ! BetterComments: índices mínimos para performance y consistencia
    await col.create_index([("codigo", ASCENDING)], unique=True, name="ux_locales_codigo")
    await col.create_index([("status", ASCENDING)], name="ix_locales_status")
    await col.create_index([("pabellon", ASCENDING)], name="ix_locales_pabellon")
    await col.create_index([("area_m2", ASCENDING)], name="ix_locales_area_m2")
    await col.create_index([("precio_mensual", ASCENDING)], name="ix_locales_precio_mensual")


async def run(drop: bool) -> None:
    client = AsyncMongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=4000)
    await client.aconnect()
    await client.admin.command("ping")

    db = client[settings.mongodb_db]
    col = db[LOCALES_COLLECTION]

    await ensure_indexes(col)

    if drop:
        await col.delete_many({})

    docs = seed_data()
    try:
        await col.insert_many(docs, ordered=False)
    except Exception:
        # Si ya existían algunos por codigo unique, no rompemos el seed (ordered=False).
        pass

    total = await col.count_documents({})
    disponibles = await col.count_documents({"status": STATUS_DISPONIBLE})
    print(f"Seed OK: total={total}, disponibles={disponibles}")

    client.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drop", action="store_true", help="Borra la colección antes de insertar.")
    args = parser.parse_args()

    asyncio.run(run(drop=args.drop))


if __name__ == "__main__":
    main()
