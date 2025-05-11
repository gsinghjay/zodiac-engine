# Technical Context: Zodiac Engine

## 1. Core Technologies

- **Programming Language**: Python (3.10+ recommended)
- **Web Framework**: FastAPI (>=0.112.0)
- **Astrology Library**: Kerykeion (==4.25.3)
- **Data Validation**: Pydantic v2 (>=2.11.0)
- **Template Engine**: Jinja2 (>=3.1.2)
- **SVG Conversion**: CairoSVG for SVG to PNG/PDF conversion, Pillow for further image processing
- **Async Support**: Primarily via FastAPI and `asyncio`, potentially `anyio` via testing setup.
- **Web Server**: Uvicorn (standard)
- **LLM Integration**: Google's Gemini API for astrological interpretations

## 2. Key Dependencies

(Refer to `requirements.txt` for specific versions)

- `fastapi`: Core FastAPI framework.
- `uvicorn[standard]`: ASGI server.
- `pydantic`: Data validation and serialization.
- `pydantic-settings`: Configuration management with environment variable support.
- `kerykeion`: Core astrology calculation and visualization engine.
- `pyswisseph`: Swiss Ephemeris binding used by Kerykeion.
- `cairosvg`: Library for converting SVG to PNG and PDF formats.
- `pillow`: Python Imaging Library, used for JPEG conversion and image manipulation.
- `Jinja2`: Template engine for web interface.
- `python-multipart`: For form data parsing.
- `pytest`, `pytest-asyncio`: For testing.
- `requests`, `requests-cache`: Used by Kerykeion for potential online features (like geonames integration).
- `python-dotenv`: Loading environment variables from `.env` file.
- `google-generativeai`: Google's Gemini API client for LLM interpretations.
- `markdown`: Library for converting Markdown to HTML, used for formatting LLM output.

## 3. Development Setup

- **Environment Management**: Standard Python virtual environments (`venv`).
- **Installation**: `pip install -r requirements.txt`.
- **Configuration**: Create a `.env` file in the project root with required environment variables:
  ```
  PROJECT_NAME="Zodiac Engine API"
  VERSION="1.0.0"
  API_V1_STR="/api/v1"
  ALLOWED_ORIGINS="*"
  GEONAMES_USERNAME="your_geonames_username" # Required for city/timezone lookup
  ```
  *Note: Ensure this file is UTF-8 encoded and correctly formatted. Debugging has shown potential issues with loading values from this file.*
- **Running Locally**: `uvicorn app.main:app --reload`.
- **Testing**: `pytest` command in the project root.
- **Version Control**: Git, hosted on GitHub.
- **CI/CD**: GitHub Actions for Semantic Release (`.github/workflows/semantic-release.yml`).

## 4. Technical Constraints & Considerations

- **Kerykeion Dependency**: The application's core functionality is tightly coupled to the Kerykeion library. Updates or changes in Kerykeion might require significant adaptation.
- **Swiss Ephemeris**: Kerykeion relies on `pyswisseph`. Ensure compatibility if system environments change.
- **SVG Conversion**: CairoSVG has some limitations with modern CSS features (like CSS variables), requiring preprocessing of SVG files before conversion.
- **System Dependencies**: CairoSVG requires system libraries (cairo, pango, etc.) to be installed on the host system, which might affect deployment options.
- **Geonames Integration**: Kerykeion uses Geonames for timezone lookups. Requires a `GEONAMES_USERNAME` environment variable loaded via `.env`. This integration is currently experiencing issues related to reading the username from the `.env` file.
- **SVG Output**: Chart visualization currently outputs SVG files stored locally. Consider implications for scaling or serverless deployments (storage, access).
- **Performance**: Complex astrological calculations or mass SVG generation could be resource-intensive. Caching and background tasks are potential optimizations.
- **Environment Configuration**: All configuration is managed through `.env` files and the `Settings` class. No hardcoded fallbacks are used.
- **Static Directory Structure**: The SVG directory must exist within the static directory for chart images to be saved correctly. Application handles this through the `initialize_static_dirs()` function.
- **API Structure Reorganization (Planned)**: The web interface routes in `app/api/web.py` are planned to be moved to a dedicated web folder (`app/api/web/`) and split into smaller, more focused modules based on functionality. This will improve code organization and maintenance but will require careful updating of imports and ensuring tests continue to pass.

## 5. Tool Usage Patterns

- **FastAPI**: Used for routing (within `app/api/v1/routers/`), dependency injection, request/response handling, OpenAPI documentation.
  - Current web interface routes located in `app/api/web.py`
  - Planned reorganization will move web routes to `app/api/web/` folder with focused modules
- **Pydantic v2**: Used for defining data schemas (validation, serialization), configuration management with modern syntax.
- **Kerykeion**: Used for all core astrological calculations and SVG generation.
- **CairoSVG**: Used for converting SVG files to PNG and PDF formats.
- **Pillow**: Used for converting PNG to JPEG and other image manipulations.
- **SVG Preprocessing**: Custom regex-based utilities to handle CSS variables in SVG files.
- **Jinja2**: Used for rendering HTML templates for the web interface.
- **FastAPI Form Processing**: Used for handling form submissions in the web interface.
- **FastAPI Background Tasks**: Used for asynchronous processing of chart generation.
- **FastAPI StaticFiles**: Used for serving static files (CSS, JavaScript, generated SVGs).
- **Google Gemini API**: Used to generate astrological interpretations from chart data.
- **Markdown**: Used to convert Gemini's Markdown output to properly formatted HTML.
- **Thread Pool**: Used via `starlette.concurrency.run_in_threadpool` to handle blocking API calls in async routes.
- **Pytest**: Used for writing and running unit and integration tests.
- **Git/GitHub**: Used for version control and CI (Semantic Release).
- **Uvicorn**: Used as the ASGI server for local development and production deployment. 
- **Dependency Injection**: Annotated types and factory functions used for modern, type-safe DI pattern. 