# Project Overview — Zodiac Engine

> Generated: 2026-06-14 · Scan level: exhaustive · Mode: initial scan

## Purpose

**Zodiac Engine** is a FastAPI web application for **astrological chart generation, visualization, tabular reporting, and AI-powered interpretation**. It wraps the [Kerykeion](https://github.com/g-battaglia/kerykeion) astrology library (exact-pinned `4.25.3`) behind:

1. A **JSON REST API** under `/api/v1` (chart data, SVG generation, reports, LLM interpretations, geo search), and
2. A **server-rendered web UI** (Jinja2 + HTMX + Bootstrap 5) for non-developer users.

It was built as an academic/portfolio project (see `README.md`) and supports both **Western (Tropical)** and **Vedic (Sidereal)** chart styles.

## Executive Summary

| Aspect | Detail |
| --- | --- |
| **Repository type** | Monolith, single Python package (`app/`) |
| **Project type** | `backend` (FastAPI service) **+ embedded server-rendered web layer** |
| **Primary language** | Python 3.12 |
| **Web framework** | FastAPI `>=0.112,<0.113` on Uvicorn |
| **Data validation** | Pydantic v2 (`2.11.x`) + pydantic-settings |
| **Astrology engine** | Kerykeion `4.25.3` (exact pin) + pyswisseph |
| **Templating / UI** | Jinja2 `3.1.x`, HTMX `2.0.4`, Bootstrap `5.3.2` (CDN) |
| **Rasterization** | CairoSVG `2.7.x` + Pillow `11.x` (system Cairo libs required) |
| **LLM interpretation** | Provider-agnostic via `LLM_*` env; **only Gemini implemented** |
| **Persistence** | **In-memory dict only** (SQLAlchemy/Alembic declared but unused) |
| **Tests** | pytest + FastAPI `TestClient` (mostly integration) |
| **Release** | python-semantic-release on push to `main` (Conventional Commits) |
| **App code size** | ~4,437 LOC across ~30 `.py` files in `app/` |

## Architecture at a Glance

Layered architecture with strict separation of concerns:

```
HTTP (JSON API + HTMX web)  →  api/ routers  →  core/ dependencies (DI)  →  services/  →  Kerykeion / GeoNames / LLM
                                    │                                          │
                              schemas/ (Pydantic)                       app/static/images/svg (generated SVG files)
```

- **`api/`** — routers only: parse request → call service → shape response. Two trees: versioned JSON API (`api/v1/...`) and the web UI (`api/web.py`).
- **`services/`** — all business logic: Kerykeion calls, SVG generation, file conversion, reports, LLM interpretation, geo lookup. Plain classes, injected via `core/dependencies.py`.
- **`schemas/`** — Pydantic v2 request/response models, one module per domain.
- **`core/`** — config (singleton `settings`), DI providers, domain exceptions, global error handlers, SVG utilities.

See [architecture.md](./architecture.md) for the full breakdown and [source-tree-analysis.md](./source-tree-analysis.md) for the annotated tree.

## What This Service Does (capability map)

| Capability | Entry point(s) | Service | Output |
| --- | --- | --- | --- |
| Natal chart **data** | `POST /api/v1/charts/natal/` | `AstrologyService` | JSON (planets, houses, aspects) |
| Natal/Synastry **SVG** | `POST /api/v1/charts/visualization/{natal,synastry}` | `ChartVisualizationService` | SVG file + URL (background task) |
| Natal/Synastry **report** | `POST /api/v1/charts/reports/{natal,synastry}` | `ReportService` | ASCII-table report (JSON) |
| **AI interpretation** | `POST /api/v1/charts/interpretations/{natal,synastry}` | `InterpretationService` | HTML interpretation (LLM) |
| **City/timezone search** | `GET /api/v1/geo/search` | `GeoService` | JSON locations (GeoNames) |
| **Web UI** (forms, charts, reports, interpret, download) | `GET /`, `/home`, `/chart/{id}`, … | all of the above | HTML / HTMX fragments |

> ⚠️ **Synastry interpretation** is a stub (returns a placeholder). **Composite / transit** charts are placeholder routers and are **not even wired into the app**. Non-SVG **web downloads (PNG/PDF/JPG)** are currently **broken** — see [architecture.md → Known Issues](./architecture.md#known-issues--gotchas).

## Key Constraints for Contributors / AI agents

These are the non-obvious rules that govern safe changes (full detail in `_bmad-output/project-context.md`):

- **Kerykeion is exact-pinned** (`==4.25.3`) — its API breaks between minor versions. Do not bump without testing. A vendored copy lives in `libraries/kerykeion/4.25.3/` (git-ignored).
- **Pydantic v2 syntax only** (`Field(..., description=...)`, `model_config`, `json_schema_extra`). No v1 `class Config`/`@validator`/`.dict()`.
- **Kerykeion is synchronous & CPU-bound** — wrap blocking calls (chart calc, CairoSVG/Pillow, file I/O) in `starlette.concurrency.run_in_threadpool` inside async routes.
- **Raise domain exceptions** (`core/exceptions.py` subclasses), not bare `HTTPException`, so the global error envelope stays consistent.
- **In-memory state is not persistence** — `web.py` `chart_cache` is per-process and lost on restart. Don't assume a database until the SQLAlchemy stack is wired up.
- **Conventional Commits are mandatory** — they drive automated versioning/CHANGELOG via python-semantic-release. Never hand-edit the version or `CHANGELOG.md`.

## Related Documentation

- [index.md](./index.md) — master navigation
- [architecture.md](./architecture.md) — components, data flow, patterns, known issues
- [api-contracts.md](./api-contracts.md) — every endpoint, request/response shapes
- [data-models.md](./data-models.md) — Pydantic schemas & domain types
- [component-inventory.md](./component-inventory.md) — web UI templates & fragments
- [development-guide.md](./development-guide.md) — setup, run, test
- [deployment-guide.md](./deployment-guide.md) — release pipeline & runtime requirements
- `../README.md` — original project README (academic write-up, mermaid diagrams)
- `../_bmad-output/project-context.md` — AI agent implementation rules
