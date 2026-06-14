# Data Models — Zodiac Engine

> Generated: 2026-06-14 · Exhaustive scan. All models are **Pydantic v2** (`Field(..., description=...)`, `model_config`, `json_schema_extra`). There is **no database schema** — the declared SQLAlchemy/Alembic stack is unused, so "data models" here means request/response and domain models.

## Overview

| Module | Models |
| --- | --- |
| `app/schemas/natal_chart.py` | `PlanetPosition`, `NatalChartRequest`, `AspectInfo`, `HouseSystem`, `NatalChartResponse` |
| `app/schemas/chart_visualization.py` | Literal types + `AspectConfiguration`, `ChartConfiguration`, `NatalChartVisualizationRequest`, `SynastryChartVisualizationRequest`, `ChartVisualizationResponse` (+ `Natal`/`Synastry` subclasses) |
| `app/schemas/report.py` | `NatalReportRequest`, `SynastryReportRequest`, `NatalReportResponse`, `SynastryReportResponse`, `NatalReportData`, `PersonReportData`, `SynastryReportData`, `InterpretationRequest`, `InterpretationResponse` |
| `app/services/geo_service.py` | `GeoLocation` (defined alongside the service) |

---

## 1. Natal chart models (`schemas/natal_chart.py`)

### `PlanetPosition`
| Field | Type | Notes |
| --- | --- | --- |
| `name` | `str` | Planet/point name |
| `sign` | `str` | Zodiac sign |
| `position` | `float` | Degrees |
| `house` | `int \| str` | House number **or** name (`"First_House"`) — normalized via `_convert_house_number` |
| `retrograde` | `bool` | — |

### `NatalChartRequest`
`name:str`, `birth_date:datetime`, `city/nation/lng/lat/tz_str: str|float|None`, `houses_system:str|None="P"`.
Location rule enforced in the **router**, not the schema: `(city+nation)` OR `(lng+lat)`.

### `AspectInfo`
`p1_name:str`, `p2_name:str`, `aspect:str`, `orbit:float`.

### `HouseSystem`
`name:str` (full name), `identifier:str` (single letter).

### `NatalChartResponse`
`name`, `birth_date`, `planets: list[PlanetPosition]`, `houses: dict[int,float]` (cusps 1..12 → degrees), `aspects: list[AspectInfo]`, `house_system: HouseSystem`. Returned with `response_model_exclude_unset=True`.

---

## 2. Visualization models (`schemas/chart_visualization.py`)

### Literal/enum types (mirror Kerykeion literals)
| Type | Values |
| --- | --- |
| `ZodiacType` | `Tropic`, `Sidereal` |
| `SiderealMode` | `FAGAN_BRADLEY`, `LAHIRI`, `DELUCE`, `RAMAN`, `USHASHASHI`, `KRISHNAMURTI`, `DJWHAL_KHUL`, `YUKTESHWAR`, `JN_BHASIN`, `BABYL_KUGLER1/2/3`, `BABYL_HUBER`, `BABYL_ETPSC`, `ALDEBARAN_15TAU`, `HIPPARCHOS`, `SASSANIAN`, `J2000`, `J1900`, `B1950` |
| `PerspectiveType` | `Apparent Geocentric`, `Heliocentric`, `Topocentric`, `True Geocentric` |
| `Planet` | Sun…Pluto, `Mean_Node`, `True_Node`, `Mean_South_Node`, `True_South_Node`, `Chiron`, `Mean_Lilith` |
| `AxialCusps` | `Ascendant`, `Medium_Coeli`, `Descendant`, `Imum_Coeli` |
| `AspectName` | `conjunction`, `semi-sextile`, `semi-square`, `sextile`, `quintile`, `square`, `trine`, `sesquiquadrate`, `biquintile`, `quincunx`, `opposition` |

### `AspectConfiguration`
`name: AspectName`, `orb: float`.

### `ChartConfiguration` (defaults shown)
| Field | Type | Default |
| --- | --- | --- |
| `houses_system` | `str` | `"P"` |
| `zodiac_type` | `ZodiacType` | `"Tropic"` |
| `sidereal_mode` | `SiderealMode \| None` | `None` (required when `zodiac_type="Sidereal"`) |
| `perspective_type` | `PerspectiveType` | `"Apparent Geocentric"` |
| `active_points` | `list[Planet \| AxialCusps]` | Sun…Pluto, Mean_Node, Chiron, Ascendant, Medium_Coeli, Mean_Lilith, Mean_South_Node |
| `active_aspects` | `list[AspectConfiguration]` | conjunction/opposition orb 10, trine 8, sextile 6, square 5, quintile 1 |

### `NatalChartVisualizationRequest`
Natal birth fields with **`birth_date` as ISO string** (not datetime), `chart_id:str|None`, `theme:str="dark"`, `language:str="EN"`, `config: ChartConfiguration|None`.

### `SynastryChartVisualizationRequest`
Two-person variant: `name1/birth_date1/city1/.../tz_str1` and `name2/.../tz_str2`, plus shared `chart_id`, `theme`, `language`, `config`.

### Responses
`ChartVisualizationResponse { chart_id:str, svg_url:str }`; `NatalChartVisualizationResponse` / `SynastryChartVisualizationResponse` are empty subclasses.

---

## 3. Report & interpretation models (`schemas/report.py`)

### Requests
- `NatalReportRequest` — like `NatalChartRequest` (datetime birth_date, optional location, `houses_system="P"`).
- `SynastryReportRequest` — two-person variant + shared `houses_system`.

### Responses
- `NatalReportResponse` — `title`, `data_table`, `planets_table`, `houses_table`, `full_report` (all `str`, ASCII tables).
- `SynastryReportResponse` — `person1: Dict[str,str]`, `person2: Dict[str,str]`.

### Structured data (interpretation inputs)
- `NatalReportData` — same five string fields as `NatalReportResponse`; passed to `InterpretationService`.
- `PersonReportData` — `title`, `data_table`, `planets_table`, `houses_table` (no `full_report`).
- `SynastryReportData` — `person1: PersonReportData`, `person2: PersonReportData`, `aspects_table: str|None`.

### Interpretation I/O
- `InterpretationRequest` — `report_data: Union[NatalReportData, SynastryReportData]`, `interpretation_type:str`, focus flags (`aspects_focus`, `compatibility_focus`, `houses_focus`, `planets_focus`, all default `True`), `tone:str="neutral"`, `max_length:int|None`.
- `InterpretationResponse` — `interpretation:str`, `highlights: list[str]`, `suggestions: list[str]` (`default_factory=list`).

> **Field-name gotcha:** the service returns `interpretation_html`, but the response model field is `interpretation`. See [api-contracts.md §B.4](./api-contracts.md#b4-interpretations-llm--chartsinterpretationspy).

---

## 4. Geo model (`services/geo_service.py`)

### `GeoLocation`
`name:str`, `country_code:str`, `latitude:float`, `longitude:float`, `timezone:str`. Returned by `GET /api/v1/geo/search`.

---

## 5. Settings model (`core/config.py`)

`Settings(BaseSettings)` — loaded from `.env` (case-sensitive).

| Field | Type | Default | Required |
| --- | --- | --- | --- |
| `PROJECT_NAME` | `str` | — | ✅ |
| `VERSION` | `str` | — | ✅ |
| `API_V1_STR` | `str` | — | ✅ |
| `ALLOWED_ORIGINS` | `str` (comma-sep) | — | ✅ (parsed by `allowed_origins_list`) |
| `GEONAMES_USERNAME` | `str` | — | ✅ (falls back to `demo` at runtime if blank) |
| `LLM_API_KEY` | `str\|None` | `None` | — |
| `LLM_MODEL_NAME` | `str\|None` | `None` | — |
| `LLM_PROVIDER` | `str\|None` | `"openai"` | — (only `gemini` implemented) |
| `LLM_MAX_TOKENS` | `int\|None` | `2000` | — |
| `LLM_TEMPERATURE` | `float\|None` | `0.7` | — |
| `LLM_CACHE_ENABLED` | `bool\|None` | `True` | — |
| `LLM_CACHE_TTL_HOURS` | `int\|None` | `24` | — |

> `config.py` uses legacy `Optional`/`List` imports while the rest of the codebase prefers `X | None`. Helper props: `allowed_origins_list`, `llm_config`.

---

## 6. Domain reference data (not Pydantic models)

- **`HOUSE_SYSTEM_MAP`** (`chart_visualization.py` and a near-duplicate in `report.py`): human name → single-letter identifier (`Placidus→P`, `Whole Sign→W`, `Koch→K`, …). Default fallback `P`.
- **House cusps** are keyed `1..12`; values are cusp longitudes in degrees.
- **`chart_cache` entry** (web, in-memory dict): `{ name, birth_date (formatted "Month D, YYYY at H:MM AM"), city, nation, lat, lng, houses_system, chart_type, theme, language }`.

## Persistence note

No ORM models, tables, or migrations exist. If/when the declared SQLAlchemy 2.0 + aiosqlite + Alembic stack is wired up, this document should be extended with the schema. Today, treat all of the above as **transient** (request/response + in-memory + on-disk SVG files).
