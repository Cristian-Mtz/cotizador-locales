# Cotizador de Locales (Backend)

Backend con **FastAPI + MongoDB (PyMongo Async)** siguiendo una arquitectura pensada para mantenibilidad:

- `routers/` -> capa HTTP (validación básica, status codes, response models)
- `services/` -> reglas de negocio (normalización, validaciones, cálculos)
- `crud/` -> persistencia (Mongo)
- `schemas/` -> DTOs (Pydantic)
- `models/` -> nombres de colecciones/constantes
- `utils/` -> helpers comunes (normalización, mapeo _id->id)
- `db.py` -> lifespan, conexión y indexes

## Requisitos

- Python **3.11 o 3.12** (recomendado 3.12). Evita pre-releases como **3.14**.
- MongoDB local: `mongodb://localhost:27017` (o Docker)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt

cp .env.example .env
docker compose up -d
```

## Run

```bash
make dev
```

Swagger:
- http://127.0.0.1:8000/docs

## Seed de locales

```bash
make seed-drop
```

## Endpoints (ejemplos curl)

Health
```bash
curl -s http://127.0.0.1:8000/api/health | jq .
```

Locales (lista)
```bash
curl -s "http://127.0.0.1:8000/api/locales?page=1&page_size=10&pabellon=A&precio_max=20000" | jq .
```

Locales (detalle)
```bash
curl -s "http://127.0.0.1:8000/api/locales/L-A-001" | jq .
```

Cotizaciones (crear)
```bash
curl -s -X POST "http://127.0.0.1:8000/api/cotizaciones" \
  -H "Content-Type: application/json" \
  -d '{"prospecto_email":"demo@mail.com","local_codigo":"L-A-001","duracion_meses":6,"notas":"Prueba"}' | jq .
```

Cotizaciones (listar por email)
```bash
curl -s "http://127.0.0.1:8000/api/cotizaciones/prospecto/demo@mail.com" | jq .
```

### Exportar OpenAPI

```bash
make openapi
```

## Decisiones técnicas

- PyMongo Async para acceso a Mongo (driver oficial).
- `created_at` se guarda en UTC (timezone-aware).
- Estandarización de errores con `AppError` -> `{ "error": { "code", "message" } }`.

## Mejoras futuras (no funcionales)

- CI (GitHub Actions) con lint/type/test
- coverage gates
- estructurar logs como JSON para producción
