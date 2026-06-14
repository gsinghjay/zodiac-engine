# Deployment Guide — Zodiac Engine

> Generated: 2026-06-14 · Exhaustive scan. **No container or Infrastructure-as-Code is committed.** The only automation is a release pipeline. This guide documents what exists and the runtime requirements for hosting.

## What's in the repo

| Concern | Status |
| --- | --- |
| Dockerfile / docker-compose | ❌ none |
| Kubernetes / Helm | ❌ none |
| Terraform / Pulumi / IaC | ❌ none |
| CI/CD | ✅ `.github/workflows/semantic-release.yml` (release only — no build/test/deploy job) |
| Process manager / systemd unit | ❌ none |

So "deployment" today means: run the ASGI app yourself with Uvicorn on a host that has Python 3.12, the pip dependencies, and the system Cairo libraries, with a populated `.env`.

## Release pipeline — `python-semantic-release`

`.github/workflows/semantic-release.yml`:

```yaml
on:
  push:
    branches: [ main ]
jobs:
  release:
    runs-on: ubuntu-latest
    concurrency: release
    permissions: { id-token: write, contents: write }
    steps:
      - uses: actions/checkout@v4           # fetch-depth: 0 (full history for versioning)
      - uses: python-semantic-release/python-semantic-release@master
        with: { github_token: ${{ secrets.GITHUB_TOKEN }} }
```

Behavior:
- **Triggers only on push to `main`** (PR merges).
- Parses **Conventional Commits** since the last release to compute the next semantic version and update `CHANGELOG.md` + create a GitHub release/tag.
- `concurrency: release` prevents overlapping release runs.

**Implications for contributors:**
- Commit messages must follow Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, …). The type determines the version bump.
- **Never hand-edit the version or `CHANGELOG.md`** — they are owned by the pipeline.
- Releases fire **only on `main`** — feature branches/PRs do not release.
- There is **no automated test or build gate** in this workflow; tests are run manually (see [development-guide.md](./development-guide.md#testing)).

> Note: the semantic-release config itself (version variable location, branch settings) is not in a committed `pyproject.toml`/`setup.cfg` in this scan — confirm where `python-semantic-release` reads its config before relying on bump behavior.

## Runtime requirements (for hosting the app)

| Requirement | Detail |
| --- | --- |
| Python | 3.12 |
| Python deps | `pip install -r requirements.txt` |
| **System libraries** | **Cairo** (for CairoSVG: `libcairo2`) — without it, SVG→PNG/PDF/JPG conversion fails to import/run |
| Filesystem (writable) | `app/static/images/svg/` (generated charts) and `cache/` (GeoNames SQLite cache) |
| Network egress | GeoNames API (`api.geonames.org`) and the LLM provider API (Gemini) |
| Env file | `.env` with all required keys (see below) |

### Required environment variables

```ini
PROJECT_NAME, VERSION, API_V1_STR, ALLOWED_ORIGINS, GEONAMES_USERNAME   # required
LLM_PROVIDER, LLM_API_KEY, LLM_MODEL_NAME, LLM_MAX_TOKENS, ...          # optional (AI features)
```

- `ALLOWED_ORIGINS` is a comma-separated string parsed into the CORS allow-list (`settings.allowed_origins_list`). Set real origins in production — `"*"` allows everything.
- `GEONAMES_USERNAME` blank/missing → service degrades to GeoNames `demo` (rate-limited).
- Missing `LLM_API_KEY` → interpretations return a placeholder (graceful degradation).

## Suggested run command

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
# behind a reverse proxy (nginx/caddy) for TLS; add --workers N for concurrency
```

Because Kerykeion work is CPU-bound and wrapped in `run_in_threadpool`, scale with multiple Uvicorn workers / replicas rather than relying on a single event loop.

## Operational caveats

- **State is per-process:** the web `chart_cache` is an in-memory dict — chart detail/report/interpret pages only work on the **same process** that generated the chart. **Do not run multiple workers/replicas** without first replacing `chart_cache` with shared storage, or chart links will 404/redirect on a different worker.
- **Generated SVGs are local files** under `app/static/images/svg/` — they are not shared across replicas and not cleaned up automatically. Use shared/object storage or a single node, or add cleanup.
- **DEBUG logging** is forced on (`logging.basicConfig(level=DEBUG)` in `main.py`) — noisy and may surface sensitive data in logs. Consider making the level env-driven before production.
- **No database:** persistence is in-memory + on-disk files. The SQLAlchemy/Alembic stack is declared but unimplemented — durable storage requires wiring it up first.
- **Secrets hygiene:** `.env` is git-ignored; ensure deployment injects secrets via the platform's secret store, not a committed file.

## Recommended hardening before production (not yet done)

- Add a `Dockerfile` (Python 3.12 + Cairo) and pin a process manager.
- Add a CI job that runs `pytest tests/` on PRs (the release workflow does not test).
- Replace `chart_cache` with Redis/DB and SVGs with object storage for multi-replica support.
- Make log level and CORS origins environment-specific.
- Fix the broken non-SVG download path before exposing those buttons (see [architecture.md §8](./architecture.md#8-known-issues--gotchas)).
