# Development Guide — Zodiac Engine

> Generated: 2026-06-14 · Exhaustive scan. Commands assume the repo root `/home/jay/github/zodiac-engine`.

## Prerequisites

| Requirement | Version | Why |
| --- | --- | --- |
| Python | **3.12** | Runtime |
| System Cairo libraries | — | Required by **CairoSVG** for PNG/PDF/JPG conversion (`libcairo2` / `cairo`) |
| GeoNames account | — | `GEONAMES_USERNAME` for city/timezone lookup (falls back to limited `demo`) |
| LLM API key (optional) | — | `LLM_API_KEY` for AI interpretations (only **Gemini** implemented) |

There is **no `pyproject.toml`** — dependencies live in `requirements.txt`. A virtualenv already exists at `venv/` (git-ignored).

## Installation

```bash
# from repo root
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# system Cairo (example: Debian/Ubuntu/WSL)
sudo apt-get install -y libcairo2 libcairo2-dev
```

> A vendored copy of Kerykeion 4.25.3 lives in `libraries/` (git-ignored), but the pinned `kerykeion==4.25.3` from `requirements.txt` is what the app imports.

## Configuration (`.env`)

`.env` (git-ignored) is **required** to run or test. Keys (see [data-models.md §5](./data-models.md#5-settings-model-coreconfigpy)):

```ini
PROJECT_NAME="Zodiac Engine API"
VERSION="1.0.0"
API_V1_STR="/api/v1"
ALLOWED_ORIGINS="*"               # comma-separated; "*" allows all
GEONAMES_USERNAME="<your-geonames-username>"
LLM_PROVIDER="gemini"             # only gemini is implemented
LLM_API_KEY="<your-key>"          # never commit; rotate if leaked
LLM_MODEL_NAME="gemini-1.5-flash-latest"
```

- Access config via the singleton `from app.core.config import settings`, or inject `SettingsDep`. **Never call `os.getenv` directly.**
- ⚠️ Root logging is forced to `DEBUG` in `main.py` — do not log secrets/PII; assume DEBUG output is visible.
- ⚠️ The committed-workspace `.env` currently contains a real-looking Gemini key. Treat it as sensitive and rotate if it has been shared.

## Running the application

```bash
source venv/bin/activate
uvicorn app.main:app --reload            # http://127.0.0.1:8000
```

Key URLs:
- Web UI: `http://127.0.0.1:8000/` (landing) → `/home` (generator)
- API docs: `http://127.0.0.1:8000/docs` · ReDoc `/redoc` · schema `/openapi.json`
- Health: `GET http://127.0.0.1:8000/api`

The SVG output directory `app/static/images/svg/` is created automatically at startup (`initialize_static_dirs()`).

## Testing

> ⚠️ `pytest.ini` declares `testpaths = app/tests`, which **does not exist**. Tests live in `./tests/`. Always pass the path explicitly:

```bash
pytest tests/                      # run the whole suite
pytest tests/test_charts_natal.py  # a single file
pytest tests/services/             # unit tests (file conversion)
pytest tests/ -k natal -v          # filter by name
```

Notes:
- Tests use `fastapi.testclient.TestClient(app)` and import the real `app` from `app.main` — most are **integration** tests exercising real Kerykeion calculations.
- `pytest-dotenv` loads `.env`, so tests may hit **GeoNames/online mode** — some require network and a valid `GEONAMES_USERNAME`. For offline runs, expect geo-dependent tests to vary.
- `tests/conftest.py` injects the repo root onto `sys.path`.
- Assert on response **shape / error envelope**, not exact astrological values (ephemeris-dependent).
- Naming (enforced by `pytest.ini`): files `test_*.py`, classes `Test*`, functions `test_*`.

## Manual test scripts (`scripts/`)

Bash scripts that exercise the running API with `curl` + `jq` (require the server running on `:8000`):

```bash
chmod +x scripts/test_western_chart.sh scripts/test_vedic_chart.sh
./scripts/test_western_chart.sh    # Tropical / Placidus / light theme
./scripts/test_vedic_chart.sh      # Sidereal LAHIRI / Whole Sign / classic theme
```
There are also Python helpers: `scripts/manual_test_file_conversion.py`, `scripts/test_svg_preprocessing.py`. See `scripts/README.md`.

## Coding conventions (from `_bmad-output/project-context.md`)

- **Pydantic v2 only** — `Field(..., description=...)`, `model_config`, `json_schema_extra`. No v1 `class Config`/`@validator`/`.dict()`.
- **Type hints everywhere**, modern style: `list[X]`, `int | str`, `X | None` (not `List`/`Optional` in new code).
- **Module + public-function docstrings** required.
- **Logging, not print** — module-level `logger = logging.getLogger(__name__)`. (One stray `print` remains in `web.py select_location`.)
- **Absolute imports** rooted at `app.` only.
- **Layered architecture** — keep routers thin; business logic in services; one domain per module across `schemas/`/`services/`/chart routers.
- **Wrap blocking work** (Kerykeion, CairoSVG/Pillow, file I/O) in `starlette.concurrency.run_in_threadpool` inside async routes.
- **Raise domain exceptions** (`core/exceptions.py`) so the error envelope stays consistent.
- No linter/formatter config is committed — match surrounding style (4-space indent, double quotes).

## Common development tasks

| Task | How |
| --- | --- |
| Add a new chart endpoint | New module in `app/api/v1/routers/charts/`, `include_router` in `charts/__init__.py`, add schema + service + `*Dep` alias |
| Add a new error type | Subclass `ZodiacEngineException` in `core/exceptions.py` |
| Add a service | Create class in `services/`, add provider + `Annotated` alias in `core/dependencies.py` |
| Add a config value | Add field to `Settings` in `core/config.py` + key in `.env` |
| Add an HTMX page/fragment | Template in `app/templates[/fragments]`, route in `app/api/web.py` returning `templates.TemplateResponse` |

## Git & release workflow

- **Branch naming:** `type/short-desc` (e.g. `feat/landing`, `chore/new-context`). Work on a branch, PR into `main`.
- **Conventional Commits are mandatory** (`feat:`, `fix:`, `chore:`, `docs:`, `style:`, …) — they drive python-semantic-release on push to `main`. A wrong/missing type yields a wrong release.
- **Never hand-edit** the version or `CHANGELOG.md` — semantic-release owns both.

See [deployment-guide.md](./deployment-guide.md) for the release pipeline.
