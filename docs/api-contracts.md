# API Contracts — Zodiac Engine

> Generated: 2026-06-14 · Exhaustive scan. Source of truth is the live OpenAPI schema at `/openapi.json` (`/docs`, `/redoc`). This catalog mirrors the code.

All error responses use the uniform envelope (see [architecture.md §6](./architecture.md#6-error-handling-contract)):
```json
{ "error": { "code": 400, "message": "…", "type": "ErrorType", "path": "/api/v1/…" } }
```
Validation errors (422) add a `details: [{ "loc": "...", "message": "...", "type": "..." }]` array.

---

## A. Top-level / health (`app/main.py`)

| Method | Path | Status | Description |
| --- | --- | --- | --- |
| GET | `/` | 303 → `/home` *(see note)* | Root redirect — **but shadowed by the web landing handler**; effective response is the landing page. See [architecture.md §8 #2](./architecture.md#8-known-issues--gotchas). |
| GET | `/api` | 200 | Health check → `{"status":"healthy","version":"<VERSION>"}` |
| GET | `/docs`, `/redoc`, `/openapi.json` | 200 | Swagger UI / ReDoc / OpenAPI schema (FastAPI defaults) |

---

## B. JSON API (`/api/v1`)

### B.1 Natal chart data — `charts/natal.py`

#### `POST /api/v1/charts/natal/` → `200`
Calculate full natal chart data (planets, houses, aspects).

**Request** (`NatalChartRequest`):
```json
{
  "name": "John Doe",
  "birth_date": "1990-01-01T12:00:00",
  "city": "New York",          // optional
  "nation": "US",              // optional
  "lng": -74.006,              // optional
  "lat": 40.7128,              // optional
  "tz_str": "America/New_York",// optional
  "houses_system": "P"         // optional, default "P" (Placidus)
}
```
Rules: `birth_date` required; must supply **(city + nation)** OR **(lng + lat)**. If both, coordinates win.

**Response** (`NatalChartResponse`, `response_model_exclude_unset=True`):
```json
{
  "name": "John Doe",
  "birth_date": "1990-01-01T12:00:00",
  "planets": [{ "name":"Sun","sign":"Capricorn","position":10.5,"house":1,"retrograde":false }],
  "houses": { "1": 0.0, "2": 30.0, "...": 0.0 },         // keys 1..12 → cusp degrees
  "aspects": [{ "p1_name":"Sun","p2_name":"Moon","aspect":"trine","orbit":120.0 }],
  "house_system": { "name":"Placidus","identifier":"P" }
}
```
Planets include the 10 standard bodies plus Mean/True Node, Mean/True South Node, Mean Lilith, Chiron (when available).

**Errors:** 400 `InvalidBirthDataError` / `LocationError`; 422 validation; 500 `ChartCalculationError`.

---

### B.2 Chart visualization (SVG) — `charts/visualization.py`

> Both endpoints return **`202 Accepted`** immediately and generate the SVG in a **FastAPI BackgroundTask**. The returned `svg_url` becomes valid once the task finishes writing the file.

#### `POST /api/v1/charts/visualization/natal` → `202`
**Request** (`NatalChartVisualizationRequest`): natal fields above **as strings** (`birth_date` ISO string) plus:
```json
{
  "name":"John Doe","birth_date":"1990-01-01T12:00:00",
  "city":"New York","nation":"US","lng":-74.006,"lat":40.7128,"tz_str":"America/New_York",
  "chart_id":"john_doe_natal",      // optional; auto natal_<hex8> if omitted
  "theme":"dark",                    // light|dark|dark-high-contrast|classic
  "language":"EN",                   // EN,ES,IT,FR,DE,PT,CN,RU,TR,HI
  "config": {                        // optional ChartConfiguration (see data-models.md)
    "houses_system":"P","zodiac_type":"Tropic","sidereal_mode":null,
    "perspective_type":"Apparent Geocentric",
    "active_points":["Sun","Moon","..."],
    "active_aspects":[{"name":"conjunction","orb":8}]
  }
}
```
**Response** (`NatalChartVisualizationResponse`):
```json
{ "chart_id":"natal_12345678", "svg_url":"/static/images/svg/natal_12345678.svg" }
```

#### `POST /api/v1/charts/visualization/synastry` → `202`
**Request** (`SynastryChartVisualizationRequest`): two people (`*1`/`*2` suffixed fields) + shared `chart_id`/`theme`/`language`/`config`. **Response:** `SynastryChartVisualizationResponse` (same shape; `chart_id` → `synastry_<hex8>`).

**Errors:** 422 invalid ISO date / validation; 500 on generation failure.

---

### B.3 Reports — `charts/reports.py`

> ASCII-table reports produced by Kerykeion's `Report`. Useful as LLM interpretation input.

#### `POST /api/v1/charts/reports/natal` → `200`
**Request** (`NatalReportRequest`): same fields as natal data request (`birth_date` as datetime). **Response** (`NatalReportResponse`):
```json
{ "title":"…","data_table":"…","planets_table":"…","houses_table":"…","full_report":"…" }
```

#### `POST /api/v1/charts/reports/synastry` → `200`
**Request** (`SynastryReportRequest`): two people. **Response** (`SynastryReportResponse`):
```json
{ "person1": { "title":"…","data_table":"…","planets_table":"…","houses_table":"…" },
  "person2": { "...": "..." } }
```
Synastry aspects table is **not yet implemented** (placeholder string in the service).

**Errors:** 400 missing birth date / location for either person; 500 `ReportGenerationError` (mapped to generic 500 here).

---

### B.4 Interpretations (LLM) — `charts/interpretations.py`

> Requires `LLM_*` env. Only **Gemini** is implemented; without a valid key the natal endpoint returns a placeholder. **Synastry interpretation is a stub.**

#### `POST /api/v1/charts/interpretations/natal` → `200`
**Request** (`InterpretationRequest`):
```json
{
  "report_data": { "title":"…","data_table":"…","planets_table":"…","houses_table":"…","full_report":"…" },
  "interpretation_type": "natal",      // must equal "natal" for this endpoint
  "aspects_focus": true, "houses_focus": true, "planets_focus": true,
  "compatibility_focus": true,         // used by synastry
  "tone": "neutral",                   // neutral|detailed|beginner-friendly
  "max_length": 1000                   // optional, words
}
```
**Response** (`InterpretationResponse`):
```json
{ "interpretation":"<html or text>", "highlights":["…"], "suggestions":["…"] }
```
> Note: the service returns the key `interpretation_html`, while the response model field is `interpretation`. The web fragment consumes `interpretation_html` directly; API consumers should rely on the documented `interpretation` field.

#### `POST /api/v1/charts/interpretations/synastry` → `200`
Same request with `interpretation_type:"synastry"` and `report_data` as `SynastryReportData`. **Currently returns a placeholder.**

**Errors:** 400 missing/invalid `report_data` or wrong `interpretation_type`; 500 on failure.

---

### B.5 Geolocation — `geo.py`

#### `GET /api/v1/geo/search?q=<city>&max_rows=<1..20>` → `200`
Search GeoNames for cities; each result includes timezone.

**Query:** `q` (required, **≥2 chars**), `max_rows` (default 10, 1–20).
**Response** (`List[GeoLocation]`):
```json
[{ "name":"New York","country_code":"US","latitude":40.7128,"longitude":-74.006,"timezone":"America/New_York" }]
```
**Errors:** 400 if `q` < 2 chars; depends on `GEONAMES_USERNAME` (falls back to `demo` with limits; GeoNames outages surface as 503 via the global handler).

---

## C. Web UI routes (`app/api/web.py`)

These return **HTML** (full pages or HTMX fragments), not JSON. Tag: `web`.

| Method | Path | Returns | Purpose |
| --- | --- | --- | --- |
| GET | `/` (`name=landing`) | `landing.html` | Marketing landing page |
| GET | `/home`, `/chart-generator` | `home.html` | Chart generator form (Western/Vedic tabs) |
| GET | `/chart/{chart_id}` | `chart_details.html` | Chart view; 303→`/home` if `chart_id` not in cache |
| GET | `/download-chart/{chart_id}?format=svg\|png\|pdf\|jpg&dpi=96` | file | Download chart. **Only `svg` works** (png/pdf/jpg broken — [§8 #1](./architecture.md#8-known-issues--gotchas)) |
| GET | `/chart-report/{chart_id}` | `fragments/report.html` | Render tabular report (HTMX) |
| GET | `/interpret-chart/{chart_id}?planets_focus&houses_focus&aspects_focus&tone&max_length` | `fragments/interpretation.html` | LLM interpretation (HTMX, `run_in_threadpool`) |
| GET | `/download-report/{chart_id}` | `text/plain` | Download full report as `.txt` |
| POST | `/search-location` (form `city`) | `fragments/location_results.html` or `location_fields.html` | City search (HTMX) |
| POST | `/select-location` (form city/nation/lng/lat/tz_str) | `fragments/location_fields.html` | Populate fields from selection |
| POST | `/validate-form` (form fields) | `fragments/form_validation.html` | Inline form validation |
| POST | `/generate-chart` (form) | `HX-Redirect` to `/chart/{id}` or `RedirectResponse 303` | Validate, schedule SVG background task, cache metadata |

**`/generate-chart` form fields:** `chart_type` (`western`|`vedic`), `name`, `birth_date` (ISO), `city`, `nation`, `lng`, `lat`, `tz_str`, `houses_system` (human name e.g. "Placidus"), `theme`, `language`, optional `sidereal_mode` (Vedic). Validates lat∈[-90,90], lng∈[-180,180], timezone via `pytz`, ISO date.

---

## D. Static files

| Path | Served from |
| --- | --- |
| `GET /static/...` | `app/static/` (mounted by `mount_static_files`) |
| `GET /static/images/svg/{chart_id}.svg` | Generated chart SVGs |

---

## Endpoint count summary

- **JSON API (`/api/v1`):** 1 natal + 2 visualization + 2 reports + 2 interpretations + 1 geo = **8**
- **Health/root:** `/api`, `/` = 2 (+ FastAPI docs routes)
- **Web UI:** 11 routes (some multi-path)
- **Not registered:** composite, synastry, transit chart endpoints (orphan stubs)
