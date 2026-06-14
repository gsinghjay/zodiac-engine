# Source Tree Analysis — Zodiac Engine

> Generated: 2026-06-14 · Exhaustive scan. Annotations describe purpose, entry points, and integration points.

## Repository layout (top level)

```
zodiac-engine/
├── app/                      # ★ Application package (the project source)
├── tests/                    # ⚠ Pytest suite (NOT app/tests — see note below)
├── scripts/                  # Manual/bash test scripts (curl + jq)
├── libraries/                # Vendored Kerykeion 4.25.3 (git-ignored, 3rd-party)
├── cache/                    # requests-cache SQLite for GeoNames (runtime, git-ignored)
├── docs/                     # ← THIS generated documentation (git-ignored!)
├── _bmad/ , _bmad-output/    # BMAD tooling + project-context.md AI rules
├── requirements.txt          # Single dependency manifest (no pyproject.toml)
├── pytest.ini                # ⚠ testpaths points to non-existent app/tests
├── .env                      # Required runtime config (git-ignored; holds live keys)
├── .github/workflows/        # semantic-release.yml (release on push to main)
├── CHANGELOG.md              # Owned by python-semantic-release — do not hand-edit
└── README.md                 # Academic write-up + mermaid architecture diagrams
```

## Application package — `app/` (entry point: `app/main.py` → `app:app`)

```
app/
├── main.py                   # ★ ENTRY POINT — create_application() factory builds the FastAPI `app`
│                             #   • configures DEBUG logging (logging.basicConfig)
│                             #   • CORS from settings.allowed_origins_list
│                             #   • add_error_handlers(), include_router(api_router), mount_static_files()
│                             #   • custom_openapi() schema; GET /api health; GET / (303→/home, see conflict*)
│
├── api/                      # ── HTTP layer (routers only; no business logic) ──
│   ├── __init__.py           #   assembles `router` = v1_router + web_router
│   ├── web.py                # ★ WEB UI routes (737 LOC): landing/home/chart pages, HTMX
│   │                         #   fragments, /generate-chart, downloads. Holds chart_cache = {} (in-memory!)
│   └── v1/                    # ── Versioned JSON API (prefix /api/v1) ──
│       ├── __init__.py        #   v1 router (prefix=/api/v1)
│       └── routers/
│           ├── __init__.py    #   includes charts_router + geo_router
│           ├── geo.py         #   GET /api/v1/geo/search → city/timezone lookup
│           └── charts/        # ── chart endpoints (prefix /charts) ──
│               ├── __init__.py        # includes natal, visualization, reports, interpretations
│               ├── natal.py           # POST /natal/ → JSON natal chart data
│               ├── visualization.py   # POST /visualization/{natal,synastry} → SVG (202, background)
│               ├── reports.py         # POST /reports/{natal,synastry} → ASCII-table report
│               ├── interpretations.py # POST /interpretations/{natal,synastry} → LLM HTML
│               ├── composite.py       # ⚠ ORPHAN: 501 stub, NOT included anywhere
│               ├── synastry.py        # ⚠ ORPHAN: 501 stub, NOT included anywhere
│               └── transit.py         # ⚠ ORPHAN: 501 stub, NOT included anywhere
│
├── services/                 # ── Business logic (plain classes; injected via DI) ──
│   ├── astrology.py          #   AstrologyService.calculate_natal_chart (lru_cache) → Kerykeion
│   ├── chart_visualization.py#   ChartVisualizationService → KerykeionChartSVG → writes SVG files
│   │                         #   + module-level map_house_system() + HOUSE_SYSTEM_MAP
│   ├── file_conversion.py    #   FileConversionService: SVG→png/pdf/jpg via cairosvg+Pillow
│   ├── report.py             #   ReportService → Kerykeion Report; parses ASCII tables; ReportGenerationError
│   ├── interpretation.py     #   InterpretationService → LLM (only Gemini implemented); markdown→HTML
│   └── geo_service.py        #   GeoService → GeoNames API via requests-cache CachedSession; GeoLocation model
│
├── schemas/                  # ── Pydantic v2 request/response models (one module per domain) ──
│   ├── natal_chart.py        #   PlanetPosition, NatalChartRequest/Response, AspectInfo, HouseSystem
│   ├── chart_visualization.py#   Literal types + ChartConfiguration + (Natal/Synastry)Visualization Req/Resp
│   └── report.py             #   Report Req/Resp + structured *ReportData + Interpretation Req/Resp
│
├── core/                     # ── Cross-cutting concerns ──
│   ├── config.py             #   Settings (pydantic-settings) + singleton `settings`
│   ├── dependencies.py       #   DI providers + Annotated *Dep aliases (lru_cache singletons)
│   ├── exceptions.py         #   ZodiacEngineException + InvalidBirthData/Location/ChartCalc/FileConversion
│   ├── error_handlers.py     #   Global handlers → uniform error envelope; Kerykeion string-matching
│   └── svg_utils.py          #   CSS var parse/substitute for SVG before raster conversion
│
├── templates/                # ── Jinja2 + HTMX views (rendered by app/templates/__init__.py) ──
│   ├── __init__.py           #   Jinja2Templates object + `now` global
│   ├── layout.html           #   Base layout (Bootstrap + HTMX from CDN, nav, footer)
│   ├── landing.html          #   Marketing landing page (GET /)
│   ├── home.html             #   Chart generator form (Western/Vedic tabs) + location modal JS
│   ├── chart_details.html    #   Chart view: SVG, interpret/report buttons, downloads, share
│   └── fragments/            #   HTMX partial responses
│       ├── location_fields.html, location_results.html  # city search + selection
│       ├── form_validation.html                         # inline validation results
│       ├── report.html, interpretation.html             # report/AI fragments
│       └── chart_preview.html                           # (preview card; not currently routed)
│
└── static/                   # ── Static assets ──
    ├── __init__.py           #   mount_static_files() + initialize_static_dirs() (creates images/svg/)
    └── images/svg/           #   Generated chart SVGs (natal_*, synastry_*, western_* — git-ignored)
```

\* **Root path conflict:** `web.py` registers `GET /` (`landing.html`) during `include_router`, and `main.py` later registers another `GET /` (303 redirect to `/home`). Because the web router is registered first, the **landing page handler wins** and the redirect is effectively shadowed. The `project-context.md` note that "`/` redirects to `/home`" appears to describe the intended/older behavior — verify before relying on either. See [architecture.md → Known Issues](./architecture.md#known-issues--gotchas).

## Critical folders explained

| Folder | Why it matters |
| --- | --- |
| `app/api/v1/routers/charts/` | Add a new chart type here as its own module, then `include_router` it in `charts/__init__.py`. Router prefixes **compose** (`/api/v1` + `/charts` + `/natal`). |
| `app/services/` | The only place business logic and third-party calls (Kerykeion, GeoNames, LLM) should live. Routers must stay thin. |
| `app/core/` | `dependencies.py` is the wiring hub — every service is exposed as a provider + `Annotated` alias. `error_handlers.py` defines the response envelope contract. |
| `app/static/images/svg/` | Generated chart files land here (created at startup by `initialize_static_dirs()`). Served at `/static/...`. Git-ignored. |
| `cache/` | `GeoService` keeps a 30-day SQLite cache (`requests-cache`) of GeoNames responses here. |
| `libraries/kerykeion/4.25.3/` | Vendored copy of the pinned astrology engine (git-ignored). Treat as a read-only dependency, not project source. |

## Notable file-placement gotchas

- **Tests live in `./tests/`**, but `pytest.ini` declares `testpaths = app/tests` (which does not exist). Run with an explicit path: `pytest tests/`. `tests/conftest.py` injects the repo root onto `sys.path`.
- **No `pyproject.toml`** — dependencies are in `requirements.txt` only. No linter/formatter config is committed.
- **`docs/` is git-ignored** (see `.gitignore`), so this generated documentation will not be version-controlled unless that entry is removed.

## Entry points

| Kind | Location |
| --- | --- |
| ASGI app object | `app.main:app` (run with `uvicorn app.main:app --reload`) |
| App factory | `app.main.create_application()` |
| JSON API root | `/api/v1` (health at `GET /api`, docs at `/docs`, `/redoc`, `/openapi.json`) |
| Web UI root | `/` (landing) → `/home` (generator) → `/chart/{id}` (details) |
