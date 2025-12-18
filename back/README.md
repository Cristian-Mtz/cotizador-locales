# FastAPI + MongoDB (app structure)

Estructura basada en:

- `app/` contiene la aplicación
- `routers/` endpoints
- `crud/` operaciones de BD
- `schemas/` modelos Pydantic
- `models/` modelos de persistencia
- `utils/` helpers
- `external_services/` integraciones

## Requisitos

- Python **3.11 / 3.12 recomendado** (evita pre-releases tipo 3.14)
- MongoDB en `mongodb://localhost:27017` (o via Docker)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate

python -m pip install -U pip
pip install -r requirements.txt
cp .env.example .env
python -m scripts.seed_locales --drop

uvicorn app.main:app --reload --port 8000
```

Swagger: `http://127.0.0.1:8000/docs`

Primera petición:
- `GET /api/health`

## Variables de entorno

Ver `.env.example`.

## Comandos útiles

```bash
ruff check .
ruff format .
mypy .
pytest
```
