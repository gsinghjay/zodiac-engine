---
project_name: 'zodiac-engine'
user_name: 'Jay'
date: '2026-06-14'
sections_completed: ['technology_stack', 'language_specific', 'framework_specific', 'error_handling', 'testing', 'code_quality', 'workflow', 'gotchas']
existing_patterns_found: 12
status: 'complete'
optimized_for_llm: true
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

**Runtime:** Python 3.12

**Web / API:**
- FastAPI `>=0.112,<0.113`, Uvicorn `[standard]` `0.34.x`
- Pydantic `2.11.x` (v2 API only) + pydantic-settings `2.8.x`
- Jinja2 `3.1.x` server-rendered templates + HTMX (fragment responses)

**Astrology core (pinned — do not bump without testing):**
- `kerykeion==4.25.3` (exact pin), pyswisseph `>=2.10.3.1,<3`
- pytz `<2025.0`, requests-cache, scour (SVG minify)

**SVG → raster:** CairoSVG `2.7.x`, Pillow `11.x` (system Cairo libs required)

**LLM interpretation:** provider-agnostic via `LLM_*` env vars
(`LLM_PROVIDER` ∈ openai/anthropic/gemini)

**Declared but NOT yet wired in:** SQLAlchemy `2.0.x` + aiosqlite + Alembic
(no models/migrations exist yet — persistence is currently in-memory dicts)

**Testing:** pytest `<8.4`, pytest-asyncio, pytest-dotenv

**Release:** python-semantic-release on `main` push (Conventional Commits drive versioning)

> Critical version constraints: **Kerykeion is exact-pinned** (API breaks between minor
> versions), **Pydantic v2 syntax only** (no v1), and the **SQLAlchemy stack is declared
> but unused** — do not assume a database exists.

## Critical Implementation Rules

### Language-Specific Rules (Python 3.12)

- **Type hints everywhere.** Use modern builtin generics and unions: `list[X]`,
  `dict[int, float]`, `int | str`, `X | None` — NOT `List`/`Optional` from typing
  in new code (schemas already use `int | str`, `str | None`).
- **Pydantic v2 only.** Use `Field(..., description=...)`, `model_config = {...}` /
  `SettingsConfigDict`, and `json_schema_extra` for examples. Never use v1
  `class Config`, `@validator`, or `.dict()`/`.parse_obj()`.
- **Module docstrings required** — every `.py` starts with a `"""..."""` one-liner;
  every public function/method has a docstring (Args/Returns style in services).
- **Logging, not print.** Module-level `logger = logging.getLogger(__name__)`;
  `logger.info` for operations, `logger.debug` for data detail.
- **Absolute imports only**, always rooted at `app.` (e.g. `from app.services.astrology
  import AstrologyService`). No relative imports.
- **Kerykeion is synchronous & CPU-bound.** In async routes, wrap blocking Kerykeion /
  file-conversion calls in `starlette.concurrency.run_in_threadpool` (see `web.py`).
- **Settings access:** import the singleton `from app.core.config import settings`, or
  inject `SettingsDep` in routes. Never call `os.getenv` directly for config.

### Framework-Specific Rules (FastAPI)

**Layered architecture — keep responsibilities separate:**
- `api/` routers = HTTP I/O only (parse request → call service → shape response).
- `services/` = all business logic / Kerykeion / LLM / file work. No FastAPI imports
  in services beyond what's needed; services are plain classes.
- `schemas/` = Pydantic request/response models (one module per domain).
- `core/` = config, dependencies, exceptions, error handlers, shared utils.

**Dependency Injection convention:**
- Every service is exposed as a `provider` function + an `Annotated[...]` alias in
  `core/dependencies.py` (e.g. `AstrologyServiceDep = Annotated[AstrologyService,
  Depends(get_astrology_service)]`). Routes inject the alias, never instantiate
  services directly.
- Stateless services use `@lru_cache` singletons. Services needing settings
  (`ChartVisualizationService`, `InterpretationService`) take `SettingsDep` and are
  NOT lru_cached.

**Router nesting (prefixes compose, don't repeat):**
- `main` → `app.api.router` → `v1` (`/api/v1`) → `charts` (`/charts`) →
  leaf router (e.g. `/natal`). Add a new chart type as its own module under
  `api/v1/routers/charts/` and `include_router` it in that package's `__init__.py`.
- Each leaf router declares its own `prefix`, `tags`, and rich `responses=` examples.

**OpenAPI discipline:** every endpoint gets `summary`, `description`, `tags`,
`status_code`, and documented error `responses` — match the verbose existing style.

**Web layer:** `api/web.py` returns HTML via Jinja2 `templates`; HTMX endpoints return
partial templates from `templates/fragments/`. Return full pages vs. fragments based on
the request (HTMX requests get fragments).

### Error Handling & Domain Rules

**Consistent error envelope (do not break this contract):**
All errors serialize to:
```json
{ "error": { "code": 0, "message": "string", "type": "string", "path": "string" } }
```
Global handlers in `core/error_handlers.py` produce this. Validation errors
(422) add a `details` array.

**Raise domain exceptions, not bare HTTPException:**
- Use the `ZodiacEngineException` subclasses in `core/exceptions.py`
  (`InvalidBirthDataError`, `LocationError`, `ChartCalculationError`,
  `FileConversionError`). They carry the right status code.
- Add a new error type by subclassing `ZodiacEngineException` — it auto-flows
  through the handler with the correct envelope.

**Kerykeion exceptions are remapped by string-matching** in the catch-all handler
(`InvalidDateError`→400, coordinates→400, Geonames→503). When wrapping Kerykeion,
either raise a domain exception explicitly or let this handler classify it — don't
swallow the original message.

**Domain conventions:**
- Default house system is `"P"` (Placidus). House identifiers are single letters
  (`P`, `W`, …); persist/echo the identifier, not the full name.
- Location input: accept city/nation OR lng/lat/tz_str. **If both are given,
  coordinates take precedence.**
- Houses can come back as ints OR strings ("First_House"); normalize via the
  existing `_convert_house_number` helper — don't reinvent the mapping.
- Geonames lookups require `GEONAMES_USERNAME`; missing/invalid → surface as 503.

### Testing Rules

- **⚠️ Test location gotcha:** `pytest.ini` declares `testpaths = app/tests`, but tests
  actually live in `./tests/` (root) — that declared path does not exist. Run tests
  with an explicit path: `pytest tests/`. (Fix the `testpaths` if you touch config.)
- **API tests use `TestClient(app)`** from `fastapi.testclient`, importing the real
  `app` from `app.main`. They hit live endpoints (e.g. `client.post("/api/v1/charts/
  natal/", json=...)`) — these are integration tests, not mocked units.
- **Fixtures** provide valid request payloads (e.g. `valid_natal_chart_request`);
  reuse/extend them rather than inlining dicts.
- **Naming (enforced by pytest.ini):** files `test_*.py`, classes `Test*`,
  functions `test_*`. Service tests go under `tests/services/`.
- `tests/conftest.py` injects the project root onto `sys.path`. `pytest-dotenv` loads
  `.env`, so tests needing `GEONAMES_USERNAME` / network may hit real services — keep
  that in mind for offline runs.
- Assert on the documented response shape and the error envelope, not on exact
  astrological values (Kerykeion output varies by ephemeris).

### Code Quality & Style Rules

- **File naming:** snake_case modules; one domain per module across `schemas/`,
  `services/`, and chart routers (`natal.py`, `synastry.py`, …). Package `__init__.py`
  files exist to assemble/`include_router` and re-export via `__all__`.
- **No linter/formatter config is committed** (no ruff/black/flake8). Match the
  surrounding style: 4-space indent, double-quoted strings, descriptive names.
- **Pydantic fields are self-documenting:** always pass `description=` to `Field(...)`
  and provide a realistic `json_schema_extra["example"]` on request/response models.
- Helper functions that aren't part of the public surface are module-level and
  `_underscore`-prefixed (e.g. `_convert_house_number`, `parse_birth_date_from_cache`).

### Development Workflow Rules

- **Conventional Commits are mandatory** — python-semantic-release parses them on every
  push to `main` to compute the version + CHANGELOG. Use `feat:`, `fix:`, `chore:`,
  `docs:`, `style:`, etc. (history confirms this). A wrong/missing type = wrong release.
- **Never hand-edit the version or `CHANGELOG.md`** — semantic-release owns both.
- **Branch naming:** `type/short-desc` (e.g. `feat/landing`, `chore/new-context`).
  Work on a branch and PR into `main`; releases fire only on `main`.
- `.env` is required to run/test (PROJECT_NAME, VERSION, API_V1_STR, ALLOWED_ORIGINS,
  GEONAMES_USERNAME, optional LLM_*). Never commit secrets; never hardcode config.

### Critical Don't-Miss Rules (Gotchas)

- **In-memory state is not persistence.** `web.py` uses a module-level `chart_cache = {}`
  dict (explicitly commented "use a database in production"). It is per-process and lost
  on restart — don't build features assuming durable storage until the SQLAlchemy stack
  is actually wired up.
- **`@functools.lru_cache` on the AstrologyService method** (`calculate_natal_chart`)
  caches on `(self, *args)` — it keeps `self` alive and shares cache across instances.
  All args must stay hashable (no dicts/lists). Be cautious adding mutable params.
- **`lru_cache`'d DI services hold one instance for the process** — keep services
  stateless. Don't store per-request data on a service that's `@lru_cache`-injected.
- **Wrap blocking work in `run_in_threadpool`** inside async routes (Kerykeion calcs,
  CairoSVG/Pillow conversion, file I/O) or you block the event loop.
- **Root logging is forced to DEBUG** in `main.py` (`logging.basicConfig(level=DEBUG)`).
  Don't log secrets/PII; assume DEBUG output is visible.
- **CORS is env-driven:** `ALLOWED_ORIGINS` is a comma-separated string parsed by
  `settings.allowed_origins_list`. Add origins via env, not code.
- **Generated SVGs/images live under `app/static/images/svg/`** and are created at
  startup by `initialize_static_dirs()`. Write generated assets there; don't hardcode
  absolute paths.
- **LLM provider is pluggable** — never assume OpenAI. Read `LLM_PROVIDER`/`LLM_MODEL_NAME`
  from settings; interpretation must degrade gracefully when `LLM_API_KEY` is unset.
- **Root `/` redirects (303) to `/home`**; health check is `GET /api`. Don't repurpose `/`.

---

## Usage Guidelines

**For AI Agents:**
- Read this file before implementing any code in zodiac-engine.
- Follow ALL rules exactly as documented; when in doubt, prefer the more restrictive option.
- Respect the layered architecture (api → services → schemas → core) and the error envelope.
- Update this file if new, durable patterns emerge.

**For Humans (Jay):**
- Keep this file lean and focused on what agents would otherwise miss.
- Update when the stack changes — especially if SQLAlchemy/Alembic get wired up
  (several gotchas here assume in-memory persistence) or the Kerykeion pin moves.
- Fix the `pytest.ini` `testpaths` discrepancy and this note can be removed.
- Review periodically and prune rules that become obvious.

Last Updated: 2026-06-14
