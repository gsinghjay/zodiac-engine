# Component Inventory — Zodiac Engine (Web UI)

> Generated: 2026-06-14 · Exhaustive scan. This project's "components" are **Jinja2 templates + HTMX fragments** (there is no JS component framework — Bootstrap 5 + HTMX over CDN, no build step).

## Rendering setup

- Templates configured in `app/templates/__init__.py`: `Jinja2Templates(directory=app/templates)` exposed as `templates`, with a global `now(fmt)` helper.
- Front-end libraries are loaded from CDN in `layout.html`: **Bootstrap 5.3.2** (CSS+JS), **HTMX 2.0.4**, plus **Bootstrap Icons** in `chart_details.html`.
- A project stylesheet is referenced at `/static/styles.css` (served from `app/static/`).
- Pattern: server returns **full pages** for direct navigation and **HTML fragments** for HTMX requests (driven by `hx-*` attributes / the `HX-Request` header).

## Page templates (full pages — extend `layout.html`)

| Template | Route(s) | Purpose | Key interactions |
| --- | --- | --- | --- |
| `layout.html` | — (base) | Shell: header gradient, navbar (Home / Generate Chart), footer with `{{ version }}`, CDN includes, `{% block %}` slots | — |
| `landing.html` | `GET /` | Marketing hero + feature cards + AI highlight + CTA | Links to `/home` |
| `home.html` | `GET /home`, `/chart-generator` | Chart generator with **Western/Vedic tabs**, location search modal | `hx-post /generate-chart`, `hx-post /validate-form` (on change), inline `fetch /api/v1/geo/search` JS modal |
| `chart_details.html` | `GET /chart/{id}` | Renders SVG + interpretation panel + report panel + download/share | `hx-get /interpret-chart/{id}`, `hx-get /chart-report/{id}`, download links, copy-link JS |

## Fragment templates (HTMX partials — `templates/fragments/`)

| Fragment | Returned by | Renders |
| --- | --- | --- |
| `location_fields.html` | `home.html` include; `/select-location`; `/search-location` | City (HTMX search), country, lng/lat, timezone `<select>` |
| `location_results.html` | `/search-location` (HTMX) | List of matched cities; each `hx-post /select-location` to fill fields |
| `form_validation.html` | `/validate-form` | Success or `<ul>` of validation errors |
| `report.html` | `/chart-report/{id}` | Title + `data/planets/houses` ASCII tables in `<pre>`; Whole-Sign note; download/print buttons |
| `interpretation.html` | `/interpret-chart/{id}` | `interpretation_html` (rendered `| safe`), highlights, suggestions, print button |
| `chart_preview.html` | *(not currently routed)* | Preview card (SVG + details table). Defined but no handler renders it |

## Key UI behaviors & conventions

- **Two chart forms** (`#western-form`, `#vedic-form`) both `hx-post` to `/generate-chart` with a hidden `chart_type`. Vedic adds a `sidereal_mode` select.
- **House system & language** are submitted as **human-readable values** (e.g. "Placidus", "en"); the backend maps them (`map_house_system`, `.upper()` for language).
- **Location flow:** two mechanisms coexist — (a) HTMX `keyup` search in `location_fields.html` → fragment results; (b) a JS modal in `home.html` calling the JSON API `GET /api/v1/geo/search` and filling fields client-side.
- **Loading states** use Bootstrap spinners gated by `.htmx-indicator` (`hx-indicator`).
- **Redirect after generate:** HTMX requests get an `HX-Redirect` header to `/chart/{id}`; non-HTMX get a 303 redirect.

## Known UI/UX issues

- **`pastel` theme option** in `home.html` is not a valid Kerykeion theme (`light/dark/dark-high-contrast/classic`) → likely fails/falls back. ([architecture.md §8 #8](./architecture.md#8-known-issues--gotchas))
- **PNG/PDF/JPEG download buttons** in `chart_details.html` point at the broken `download_chart` path (only SVG works). ([§8 #1](./architecture.md#8-known-issues--gotchas))
- `chart_preview.html` is orphaned (no route renders it).
- Timezone `<select>` in `location_fields.html` is a short hard-coded list; the JS modal appends unknown timezones dynamically, but the HTMX path does not.

## Static assets

| Asset | Location | Notes |
| --- | --- | --- |
| Generated chart SVGs | `app/static/images/svg/` | `natal_*`, `synastry_*`, `western_*` (git-ignored); created at startup |
| Referenced images | `/static/images/hero-background.svg`, `/static/images/ai-illustration.svg` | Used by `landing.html` |
| Stylesheet | `/static/styles.css` | Referenced by `layout.html` |
