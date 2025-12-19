# Cotizador de Locales — Frontend

Frontend del proyecto **Cotizador de Locales**, construido con **Angular (standalone) + TailwindCSS + NgRx** y enfocado en una arquitectura mantenible por **scopes**: `feature / ui / data-access / util`.

Este README es **solo del frontend**. Más adelante habrá un **README general en la raíz** con los **URLs de despliegue** (Front/Back).

---

## Stack

- Angular (Standalone Components) + SSR (Hydration)
- TailwindCSS
- NgRx (Store/Effects/DevTools) con patrón **data-access + facade**
- Leaflet (mapa) + OpenStreetMap tiles
- Vitest (tests)

---

## Requisitos

- **Node.js**: recomendado **LTS** (20.x o 22.x)
- **npm**
- Backend corriendo localmente (ver README del backend)

---

## Instalación

```bash
npm install
```

---

## Ejecutar en desarrollo

### 1) Levantar backend
Asegúrate de tener el backend arriba:

- `http://localhost:8000`

### 2) Levantar frontend
```bash
npm start
```

App:
- `http://localhost:4200`

---

## Conexión con el Backend (proxy)

En desarrollo usamos **proxy** para evitar CORS y mantener el frontend consumiendo `/api`:

- El navegador hace requests a: `http://localhost:4200/api/...`
- El dev server reenvía a: `http://localhost:8000/...` (según tu `proxy.conf.json`)

Esto permite que el `API_BASE_URL` sea **`/api`** en el frontend (sin hardcodear host/puerto).

> Nota importante: el API base URL **no es un secreto**; lo “seguro” es **no incluir secretos** (tokens privados, keys, etc.) en el bundle del navegador.

---

## Scripts

```bash
npm start         # dev server (con proxy)
npm run build     # build (incluye SSR si está configurado)
npm test          # tests
```

Si tu proyecto SSR tiene el script:
```bash
npm run serve:ssr:front
```

> Ajusta el script de SSR según el output real de tu build (`dist/<app>/server/server.mjs`).

---

## Rutas principales

- `/locales`  
  Vista de locales + mapa (Leaflet) + selección de local

- `/cotizaciones?local=L-A-001`  
  Crear cotización y ver historial por email

---

## Arquitectura (scope rules)

Estructura base dentro de `src/app`:

- `core/*`  
  Configuración global, tokens, utilidades de infraestructura (HTTP, etc.)

- `shared/*`  
  Componentes y utilidades reutilizables:
  - `shared/ui/*`
  - `shared/util/*`

- `locales/*` y `cotizaciones/*`  
  Features separadas por dominio:
  - `feature/*` → pages/routing
  - `ui/*` → componentes presentacionales
  - `data-access/*` → API + store NgRx + facade
  - `util/*` → helpers del dominio

Ejemplo (simplificado):

```
src/app/
  core/
    data-access/
      api-base-url.ts
      http-client.util.ts
  shared/
    ui/
    util/
  locales/
    feature/
      locales.routes.ts
      locales-page.component.*
    ui/
      map/
        locales-map-shell.component.ts
        locales-map-client.component.ts
    data-access/
      models/
      service/
      store/
      locales.facade.ts
  cotizaciones/
    feature/
      cotizaciones.routes.ts
      cotizaciones-page.component.ts
    data-access/
      models/
      service/
      store/
      cotizaciones.facade.ts
```

### Capas (responsabilidades)

- **UI/Page**: interacción y render
- **Facade**: API del feature para la UI (orquesta acciones / expone selectors)
- **Store/Effects**: flujo de estado + side-effects
- **API Service**: comunicación HTTP con el backend

---

## Flujo manual de prueba (happy path)

1) Ir a `/locales`  
2) Seleccionar un local (desde mapa o lista)  
3) Click en “Ir a cotizar” → navega a `/cotizaciones?local=...`  
4) Capturar:
   - `prospecto_email`
   - `duracion_meses`
   - (opcional) `notas`  
5) Crear cotización (POST)  
6) Ver historial por email (GET) con orden por `created_at` desc

---

## Decisiones técnicas

- **NgRx por feature (lazy)**: cada feature registra `provideState/provideEffects` a nivel de ruta.
- **Facade pattern**: la UI no conoce actions/selectors directamente.
- **Signals en UI**: `toSignal()` para consumir store sin `AsyncPipe` y usar control flow moderno (`@if`, `@for`).
- **SSR-safe Leaflet**: inicialización del mapa solo en browser (client-only) para evitar `window/document` en server.
- **HttpClient con fetch**: `withFetch()` habilitado para SSR/hydration.

---

## Tests

Siguiente paso recomendado:
- Reducers: tests unitarios para cambios de estado (create/list).
- Effects: tests con Http mocks (happy/error).
- E2E (Playwright/Cypress): flujo completo locales → cotizar → historial.

---

## “Mejoras futuras” (no funcionalidad)

- CI (GitHub Actions): `npm ci` + `npm test` + `npm run build`
- Mejor DX:
  - scripts tipo `make dev`, `make test`, `make lint` (o `taskfile`)
- UX:
  - skeleton loaders
  - estados vacíos
  - toasts
  - manejo uniforme de errores (mismo shape del backend)
- Runtime config para `API_BASE_URL` (por entorno) sin rebuild, usando SSR server o rewrites.

---

## Troubleshooting

### El proxy no aplica / sigue pegando al host viejo
Reinicia el dev server:

```bash
# Ctrl+C
npm start
```

Angular CLI no siempre recarga el proxy/config al vuelo.

### Error NG0203 (inject outside injection context)
Evita usar `inject()` dentro de helpers “puros” que se ejecuten fuera de DI.
Inyecta tokens (ej. `API_BASE_URL`) directamente en servicios / clases.

### Leaflet no carga en SSR
Asegura que Leaflet se inicializa **solo en browser** (client-only) y que el CSS de Leaflet está incluido en `styles.css`.
