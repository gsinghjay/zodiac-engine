# Technical Context: Zodiac Engine

## 1. Core Technologies

- **Programming Language**: Python (3.10+ recommended)
- **Web Framework**: FastAPI (>=0.112.0)
- **Astrology Library**: Kerykeion (==4.25.3)
- **Data Validation**: Pydantic v2 (>=2.11.0)
- **Async Support**: Primarily via FastAPI and `asyncio`, potentially `anyio` via testing setup.
- **Web Server**: Uvicorn (standard)

## 2. Key Dependencies

(Refer to `requirements.txt` for specific versions)

- `fastapi`: Core FastAPI framework.
- `uvicorn[standard]`: ASGI server.
- `pydantic`: Data validation and serialization.
- `pydantic-settings`: Configuration management with environment variable support.
- `kerykeion`: Core astrology calculation and visualization engine.
- `pyswisseph`: Swiss Ephemeris binding used by Kerykeion.
- `pytest`, `pytest-asyncio`: For testing.
- `requests`, `requests-cache`: Used by Kerykeion for potential online features (like geonames integration).
- `python-dotenv`: Loading environment variables from `.env` file.

## 3. Development Setup

- **Environment Management**: Standard Python virtual environments (`venv`).
- **Installation**: `pip install -r requirements.txt`.
- **Configuration**: Create a `.env` file in the project root with required environment variables:
  ```
  PROJECT_NAME="Zodiac Engine API"
  VERSION="1.0.0"
  API_V1_STR="/api/v1"
  ALLOWED_ORIGINS="*"
  GEONAMES_USERNAME=""
  ```
- **Running Locally**: `uvicorn app.main:app --reload`.
- **Testing**: `pytest` command in the project root.
- **Version Control**: Git, hosted on GitHub.
- **CI/CD**: GitHub Actions for Semantic Release (`.github/workflows/semantic-release.yml`).

## 4. Technical Constraints & Considerations

- **Kerykeion Dependency**: The application's core functionality is tightly coupled to the Kerykeion library. Updates or changes in Kerykeion might require significant adaptation.
- **Swiss Ephemeris**: Kerykeion relies on `pyswisseph`. Ensure compatibility if system environments change.
- **Geonames Integration**: Kerykeion can use Geonames for timezone lookups. Requires a `GEONAMES_USERNAME` environment variable (currently optional and potentially disabled in service layer).
- **SVG Output**: Chart visualization currently outputs SVG files stored locally. Consider implications for scaling or serverless deployments (storage, access).
- **Performance**: Complex astrological calculations or mass SVG generation could be resource-intensive. Caching and background tasks are potential optimizations.
- **Environment Configuration**: All configuration is managed through `.env` files and the `Settings` class. No hardcoded fallbacks are used.

## 5. Tool Usage Patterns

- **FastAPI**: Used for routing, dependency injection, request/response handling, OpenAPI documentation.
- **Pydantic v2**: Used for defining data schemas (validation, serialization), configuration management with modern syntax.
- **Kerykeion**: Used for all core astrological calculations and SVG generation.
- **Pytest**: Used for writing and running unit and integration tests.
- **Git/GitHub**: Used for version control and CI (Semantic Release).
- **Uvicorn**: Used as the ASGI server for local development and production deployment. 
- **Dependency Injection**: Annotated types and factory functions used for modern, type-safe DI pattern. 