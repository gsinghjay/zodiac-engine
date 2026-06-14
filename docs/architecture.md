# Architecture — Zodiac Engine

> Generated: 2026-06-14 · Exhaustive scan. Single-part `backend` (FastAPI) with an embedded server-rendered web layer.

## 1. Executive Summary

Zodiac Engine is a **layered FastAPI monolith**. HTTP requests enter through one of two router trees — a versioned JSON API (`/api/v1/...`) and a server-rendered HTMX web UI (`app/api/web.py`) — and are dispatched, via FastAPI dependency injection, to a set of stateless **service** classes that wrap the Kerykeion astrology engine, the GeoNames geocoding API, an LLM provider, and SVG→raster conversion. Generated chart SVGs are written to disk under `app/static/`; transient web-session chart metadata is kept in an in-process dictionary. There is **no database** in use today.

## 2. Technology Stack

| Category | Technology | Version (constraint) | Notes / Justification |
| --- | --- | --- | --- |
| Language | Python | 3.12 | Modern generics/unions used in newer modules |
| Web framework | FastAPI | `>=0.112,<0.113` | Routing, DI, OpenAPI, validation |
| ASGI server | Uvicorn `[standard]` | `>=0.34,<0.35` | Dev/prod server |
| Validation | Pydantic | `2.11.x` (v2 only) | Request/response models, settings |
| Settings | pydantic-settings | `2.8.x` | `.env`-driven `Settings` |
| Astrology engine | Kerykeion | `==4.25.3` (exact) | Charts, aspects, reports. **API breaks between minors** |
| Ephemeris | pyswisseph | `>=2.10.3.1,<3` | Swiss Ephemeris backend for Kerykeion |
| Timezones | pytz | `>=2024.2,<2025.0` | Timezone validation in web forms |
| Geocoding cache | requests-cache + requests | `1.2.x` / `2.32.x` | 30-day SQLite cache of GeoNames |
| Templating | Jinja2 | `3.1.x` | Server-rendered HTML |
| Front-end (CDN) | HTMX 2.0.4, Bootstrap 5.3.2 | — | Progressive enhancement, no build step |
| SVG → raster | CairoSVG + Pillow | `2.7.x` / `11.x` | PNG/PDF/JPG export (needs system Cairo libs) |
| SVG minify | scour | `0.38.x` | Declared dep (used by Kerykeion path) |
| Markdown | markdown | `3.6` | LLM markdown → HTML |
| LLM (impl) | google-generativeai (Gemini) | — | Only provider actually wired; openai/anthropic are config-only |
| Tables | simple-ascii-tables | `1.0.x` | Kerykeion report formatting |
| **Declared but unused** | SQLAlchemy 2.0 / aiosqlite / alembic | — | **No models or migrations exist** |
| Testing | pytest, pytest-asyncio, pytest-dotenv | `<8.4` / … | `TestClient` integration tests |
| Release | python-semantic-release | — | Versioning from Conventional Commits on `main` |

**Architecture pattern:** Layered / service-oriented (API → DI → Service → Integration). Within the web layer, an HTMX "HATEOAS-lite" pattern returns HTML fragments.

## 3. Layered Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│  CLIENTS:  Browser (HTML/HTMX)        API consumers (JSON)             │
└───────────────┬──────────────────────────────┬───────────────────────┘
                │                               │
┌───────────────▼───────────────┐   ┌───────────▼───────────────────────┐
│  app/api/web.py (web router)   │   │  app/api/v1/** (versioned JSON)    │   ← API LAYER
│  HTML pages + HTMX fragments   │   │  charts/* , geo                    │     (routers only)
└───────────────┬────────────────┘   └───────────┬───────────────────────┘
                └───────────────┬─────────────────┘
                                ▼
                   ┌────────────────────────────┐
                   │  app/core/dependencies.py  │   ← DI WIRING (Annotated *Dep aliases)
                   └────────────┬───────────────┘
                                ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │  app/services/  (plain classes, business logic)                  │   ← SERVICE LAYER
   │  Astrology · ChartVisualization · FileConversion ·               │
   │  Report · Interpretation · Geo                                   │
   └───────┬──────────────┬──────────────┬───────────────┬───────────┘
           ▼              ▼              ▼               ▼
       Kerykeion     CairoSVG/Pillow  GeoNames API   LLM (Gemini)
           │
           ▼
   app/static/images/svg/*.svg   (generated files on disk)

   Cross-cutting: app/schemas/ (Pydantic models) · app/core/{config,exceptions,error_handlers,svg_utils}
```

**Rules enforced by the codebase (and `project-context.md`):**
- Routers parse the request, call a service, and shape the response. No Kerykeion/LLM/file logic in routers.
- Services are plain classes injected through `core/dependencies.py` `Annotated[...]` aliases — routers never instantiate services directly.
- Stateless services use `@lru_cache` singletons; services that need `settings` (`ChartVisualizationService`, `InterpretationService`) take `SettingsDep` and are **not** cached.

## 4. Component Overview

### 4.1 API layer (`app/api/`)

| Component | File | Responsibility |
| --- | --- | --- |
| Root assembler | `api/__init__.py` | Combines `v1_router` + `web_router` into one `router` |
| v1 assembler | `api/v1/__init__.py`, `…/routers/__init__.py` | Prefix `/api/v1`; includes `charts` + `geo` |
| Natal data | `charts/natal.py` | `POST /natal/` → JSON natal chart |
| Visualization | `charts/visualization.py` | `POST /visualization/{natal,synastry}` → SVG (202, BackgroundTasks) |
| Reports | `charts/reports.py` | `POST /reports/{natal,synastry}` → ASCII-table report |
| Interpretations | `charts/interpretations.py` | `POST /interpretations/{natal,synastry}` → LLM HTML |
| Geo | `geo.py` | `GET /geo/search` → city/timezone list |
| **Web UI** | `web.py` | Pages + HTMX fragments + `/generate-chart` + downloads |
| Orphan stubs | `charts/{composite,synastry,transit}.py` | 501 placeholders — **not registered** (absent from `charts/__init__.py`) |

### 4.2 Service layer (`app/services/`)

| Service | Cached? | Needs settings? | Integrations | Key methods |
| --- | --- | --- | --- | --- |
| `AstrologyService` | `lru_cache` (DI) + `lru_cache` on method | no | Kerykeion `AstrologicalSubject`, `NatalAspects` | `calculate_natal_chart()` |
| `ChartVisualizationService` | **no** (takes `Settings`) | yes | Kerykeion `KerykeionChartSVG`, filesystem | `generate_natal_chart_svg()`, `generate_synastry_chart_svg()`, module `map_house_system()` |
| `FileConversionService` | `lru_cache` (DI) | no | CairoSVG, Pillow, `core/svg_utils` | `convert_svg_to_format()`, `convert_svg_file_to_format()` |
| `ReportService` | `lru_cache` (DI) | no | Kerykeion `Report` | `generate_natal_report()`, `generate_synastry_report()`, `_map_house_system()` |
| `InterpretationService` | **no** (takes LLM config) | yes | google-generativeai (Gemini), markdown | `interpret_natal_chart()`, `interpret_synastry_chart()` (stub) |
| `GeoService` | `lru_cache` (DI) | reads `settings` directly | GeoNames API via `requests-cache` | `search_cities()`, `_get_timezone()` |

### 4.3 Core (`app/core/`)

- **`config.py`** — `Settings(BaseSettings)` reads `.env` (case-sensitive). Exposes singleton `settings` and helper props `allowed_origins_list`, `llm_config`. Required keys: `PROJECT_NAME`, `VERSION`, `API_V1_STR`, `ALLOWED_ORIGINS`, `GEONAMES_USERNAME`. Optional `LLM_*`.
- **`dependencies.py`** — `get_settings`/`SettingsDep`, and one provider + `Annotated` alias per service.
- **`exceptions.py`** — `ZodiacEngineException(HTTPException)` base + `InvalidBirthDataError` (400), `LocationError` (400), `ChartCalculationError` (500), `FileConversionError` (500).
- **`error_handlers.py`** — four handlers producing the uniform error envelope (see §6).
- **`svg_utils.py`** — parses `:root` CSS variables and substitutes `var(--x)` references (multi-pass, cycle-safe) so CairoSVG can rasterize Kerykeion SVGs that use CSS custom properties.

## 5. Data Flow

### 5.1 Web chart generation (HTMX)
```
Browser form (home.html) ──POST /generate-chart (HTMX)──► web.py
  validate (pytz tz, lat/lng ranges, ISO date)
  build config (Western=Tropic / Vedic=Sidereal, active points/aspects)
  BackgroundTasks.add_task(ChartVisualizationService.generate_natal_chart_svg, ...)   # async write of SVG
  chart_cache[chart_id] = { name, birth_date(formatted), city, nation, lat, lng, ... }  # in-memory
  return HX-Redirect: /chart/{chart_id}
Browser GET /chart/{id} ──► chart_details.html (img src=/static/images/svg/{id}.svg)
  ├─ HTMX GET /chart-report/{id}      → ReportService → fragments/report.html
  ├─ HTMX GET /interpret-chart/{id}   → ReportService → InterpretationService (run_in_threadpool) → fragments/interpretation.html
  └─ GET /download-chart/{id}?format= → FileConversionService (SVG ok; png/pdf/jpg BROKEN — see §8)
```

### 5.2 JSON API natal chart
```
POST /api/v1/charts/natal/ ──► natal.py
  validate birth_date present; require (city+nation) OR (lng+lat)
  AstrologyService.calculate_natal_chart(...)  # lru_cached; Kerykeion AstrologicalSubject + NatalAspects
  → NatalChartResponse { planets[], houses{1..12}, aspects[], house_system }
  errors → ChartCalculationError → uniform envelope
```

### 5.3 Location search (two paths)
- **API/JS path:** `home.html` JS `fetch('/api/v1/geo/search?q=...')` → `geo.py` → `run_in_threadpool(GeoService.search_cities)` → JSON.
- **HTMX path:** `location_fields.html` `hx-post /search-location` → `web.py` → `GeoService.search_cities` → `fragments/location_results.html` → selecting an item `hx-post /select-location` → `fragments/location_fields.html` (fills lat/lng/tz).

## 6. Error Handling Contract

All errors serialize through `core/error_handlers.py` to a uniform envelope — **do not break this**:

```json
{ "error": { "code": 400, "message": "…", "type": "ErrorType", "path": "/api/v1/…" } }
```

- `ZodiacEngineException` subclasses → their own status code + `type` = class name.
- `RequestValidationError` / Pydantic `ValidationError` → **422** with an added `details: [{loc, message, type}]` array.
- Catch-all `Exception` handler **remaps Kerykeion errors by string-matching** `type(exc).__module__`/name/message:
  - `InvalidDateError` / "date" → 400
  - coordinates / "lat"/"lng" → 400
  - "geonames" → **503**
  - other kerykeion → 500 `AstrologyCalculationError`
  - everything else → 500 `Internal server error`

Routers therefore should **raise domain exceptions** (or let Kerykeion errors bubble) rather than swallowing messages.

### Domain conventions
- Default house system `"P"` (Placidus); identifiers are single letters. Human names map via `HOUSE_SYSTEM_MAP` (defined **twice** — see §8).
- Location: accept city/nation OR lng/lat/tz; **if both given, coordinates win**.
- Houses may return ints or strings (`"First_House"`); normalize via `_convert_house_number` in `astrology.py`.

## 7. Persistence & State

| Store | Where | Lifetime | Notes |
| --- | --- | --- | --- |
| `chart_cache` dict | `web.py` module global | Per-process, lost on restart | Holds web-session chart metadata; **not durable** |
| Generated SVGs | `app/static/images/svg/` | On disk until deleted | `natal_*`, `synastry_*`, `western_*` git-ignored |
| GeoNames cache | `cache/zodiac_geonames_cache` (SQLite) | 30 days | via `requests-cache` |
| `@lru_cache` results | process memory | Process lifetime | Natal calc method cache (maxsize 128) + DI singletons |
| **SQLAlchemy DB** | — | — | **Declared in requirements but not implemented** |

> The `@lru_cache` on `AstrologyService.calculate_natal_chart` keys on `(self, *args)` — it retains `self` and shares across instances; all args must stay hashable (no dicts/lists).

## 8. Known Issues & Gotchas

These are concrete findings from the exhaustive read — useful targets for fixes and important context before changing related code.

| # | Issue | Location | Impact |
| --- | --- | --- | --- |
| 1 | **Web PNG/PDF/JPG download is broken.** `download_chart` calls `conversion_service.convert_svg_file(...)` (no such method — it's `convert_svg_file_to_format`) and `OutputFormat(format.upper())` (calls a `Literal` type as a constructor; `"PNG"` is not even a valid member). Only `format=svg` works. | `app/api/web.py` `download_chart` | UI download buttons for PNG/PDF/JPG in `chart_details.html` raise 500 |
| 2 | **Two handlers for `GET /`.** `web.py` registers `/` (landing) first; `main.py` registers `/` (303→/home) after. The landing handler shadows the redirect. | `web.py` + `main.py` | Actual `/` behavior contradicts the "redirects to /home" note; verify before relying on either |
| 3 | **Orphan routers.** `composite.py`, `synastry.py`, `transit.py` define 501 routers but are not included in `charts/__init__.py`. | `api/v1/routers/charts/` | Endpoints don't exist; dead code |
| 4 | **Synastry interpretation is a stub** returning a placeholder; openai/anthropic providers are config-only (only Gemini implemented). | `services/interpretation.py` | `POST /interpretations/synastry` returns placeholder text |
| 5 | **Duplicated house-system mapping.** `HOUSE_SYSTEM_MAP` exists in both `chart_visualization.py` (module) and `report.py` (`_map_house_system`), with slightly different alias sets. | both services | Risk of drift; consolidate when touched |
| 6 | **`print()` instead of logger** in `select_location` — violates the "logging, not print" rule. | `web.py` | Minor; inconsistent logging |
| 7 | **`pytest.ini testpaths = app/tests`** does not exist; tests are in `./tests/`. | `pytest.ini` | Bare `pytest` collects nothing useful; use `pytest tests/` |
| 8 | **`theme` mismatch.** `home.html` offers a `pastel` theme option, but Kerykeion themes are `light/dark/dark-high-contrast/classic`. | `templates/home.html` | `pastel` likely falls back / errors at render |
| 9 | **`config.py` uses legacy typing** (`Optional`, `List`) while the rest of the codebase prefers `X | None`. | `core/config.py` | Stylistic inconsistency only |
| 10 | **Secrets in working tree.** `.env` holds a live-looking Gemini API key and GeoNames username. `.env` is git-ignored (not committed), but the key is present locally. | `.env` | Rotate the key if it was ever shared; never echo it into docs/logs (root logging is DEBUG) |

## 9. Testing Strategy

- **Framework:** pytest + `fastapi.testclient.TestClient(app)` importing the real `app` from `app.main`.
- **Style:** mostly **integration** tests that hit live endpoints and exercise real Kerykeion calculations (e.g. `tests/test_charts_natal.py`, `test_chart_configuration.py`, `test_natal_chart_variations.py`, `test_static_images.py`). `tests/services/test_file_conversion.py` is a **unit** test using mocks. `tests/test_svg_utils.py` unit-tests CSS-var substitution.
- **Assertions** target response shape / error envelope, not exact astrological values (ephemeris-dependent).
- **Network/secrets:** `pytest-dotenv` loads `.env`, so tests needing `GEONAMES_USERNAME` or online mode may hit real services — keep this in mind for offline/CI runs.
- **Run:** `pytest tests/` (the `pytest.ini` path is wrong; see issue #7).

See [development-guide.md](./development-guide.md) for commands.

## 10. Deployment Architecture

There is **no container/IaC** in the repo. The only automation is `.github/workflows/semantic-release.yml`, which runs `python-semantic-release` on push to `main` to compute the version and update `CHANGELOG.md` from Conventional Commits. Runtime requires Python 3.12, the pip dependencies, **system Cairo libraries** (for CairoSVG), and a populated `.env`. See [deployment-guide.md](./deployment-guide.md).

## 11. Extension Points (for new work)

- **New chart type:** add `app/api/v1/routers/charts/<type>.py`, then `include_router` it in `charts/__init__.py`. Add schemas in `schemas/`, logic in a service, and a `*Dep` alias in `core/dependencies.py`.
- **New error type:** subclass `ZodiacEngineException` — it auto-flows through the envelope with the right status.
- **New LLM provider:** implement the branch in `InterpretationService.__init__`/`interpret_*` keyed on `LLM_PROVIDER`; keep graceful degradation when `LLM_API_KEY` is unset.
- **Persistence:** the SQLAlchemy/aiosqlite/Alembic stack is declared — wiring it up would let `chart_cache` and chart files become durable (several gotchas assume in-memory today).
