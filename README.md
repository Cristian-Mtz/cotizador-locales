# Cotizador de Locales (Monorepo)

Monorepo con **Backend (FastAPI + MongoDB)** y **Frontend (Angular Standalone + TailwindCSS + NgRx + Leaflet)** para un flujo de **selección de local → creación de cotización → historial por email**.

---

## Demo (Deploy)

- **Frontend (Vercel):** https://cotizador-locales.vercel.app/ 
  > Nota: este enlace es del proyecto/deployment en Vercel. Si tienes un dominio público tipo `https://<app>.vercel.app`, agrégalo aquí.

- **Backend (Render) – Swagger/OpenAPI:** https://cotizador-locales.onrender.com/docs

---

## Estructura del repo

```
cotizador-locales/
  back/   # FastAPI + MongoDB
  front/  # Angular + Tailwind + NgRx + Leaflet
  README.md
```

---

## Requisitos

- Node.js (LTS recomendado 20.x/22.x) + npm
- Python 3.12 (recomendado)
- MongoDB local (para desarrollo) o MongoDB Atlas (para deploy)

---

## Setup local (Desarrollo)

### 1) Backend (FastAPI)

```bash
cd back

# Crear venv (ejemplo)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows PowerShell

pip install -r requirements.txt
```

#### Variables de entorno
Crea un `.env` en `back/` (ejemplo):

```env
ENV=local
MONGODB_URI=mongodb://localhost:27017
DB_NAME=cotizador_locales
CORS_ORIGINS=http://localhost:4200
```

#### Ejecutar
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger:
- http://localhost:8000/docs

---

### 2) Frontend (Angular)

```bash
cd front
npm install
npm start
```

App:
- http://localhost:4200

#### Comunicación Front ↔ Back (proxy recomendado)
El frontend consume el API en ruta relativa **`/api`**. En dev, se recomienda proxy (Angular/Vercel rewrites) para evitar CORS.

---

## Endpoints principales

> Nota: el prefijo puede ser `/api` según la configuración del backend.

- `GET /api/locales`  
  Lista de locales con paginación.

- `POST /api/cotizaciones`  
  Crea una cotización (email + local + duración + notas opcionales).

- `GET /api/cotizaciones/prospecto/{email}`  
  Lista historial de cotizaciones por email (ordenable en UI por `created_at` desc).

---

## Arquitectura (resumen)

### Backend
- Estructura por módulos, configuración separada (config/db/errors), handlers globales y helpers para:
  - normalización (email/códigos)
  - mapeo estable de `_id` → `id`
  - fechas UTC

### Frontend
- Standalone components
- NgRx por feature (lazy) con patrón:
  - UI/Page → Facade → Store/Effects → API Service
- Control Flow moderno (`@if`, `@for`) y consumo del store vía `toSignal()`
- Leaflet en modo SSR-safe (mapa solo en browser)

---

## Deploy

### Backend en Render (monorepo)
Config recomendado en Render (Web Service):
- **Root Directory:** `back`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:**
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- **Environment Variables:**
  - `MONGODB_URI` (Atlas)
  - `DB_NAME`
  - `CORS_ORIGINS` (si no usarás proxy)
  - `PYTHON_VERSION` (ej. `3.12.8`)

### DB en MongoDB Atlas
- Crear cluster y usuario
- Permitir acceso desde Render (IP dinámica → para demo suele usarse allow from anywhere)
- Guardar credenciales **solo** en variables de entorno (no en el repo)

### Front en Vercel (monorepo)
- **Root Directory:** `front`
- **Build Command:** `npm run build`
- **Output Directory:** carpeta donde vive `index.html` (común: `dist/<app>/browser`)
- Rewrites para `/api/*` → Render (recomendado):
  - en `front/vercel.json`:
    ```json
    {
      "rewrites": [
        { "source": "/api/(.*)", "destination": "https://cotizador-locales.onrender.com/api/$1" },
        { "source": "/(.*)", "destination": "/index.html" }
      ]
    }
    ```

> Si tu backend NO usa prefijo `/api`, cambia el destino a `https://cotizador-locales.onrender.com/$1`.

---

## Mejoras futuras (no funcionalidad)

- Tests:
  - Reducers/effects unit tests (front)
  - E2E (Playwright/Cypress)
  - Tests E2E en backend con DB efímera (testcontainers)
- CI: lint + typecheck + test + build
- Observabilidad: logging estructurado + request id
- UX: skeleton loaders, toasts, estados vacíos, mejoras del mapa (markers, clustering)

---

## Licencia
Uso educativo / prueba técnica.
