# Zodiac Engine

Astrological calculation engine powered by the [Kerykeion](https://github.com/Kerykeion/Kerykeion) library, delivered via a FastAPI backend and a user-friendly web interface.

## Features

-   **Web Interface**: Generate Western (Tropical) and Vedic (Sidereal) charts directly in your browser. Features include:
    *   City lookup using GeoNames (requires account).
    *   Customizable chart themes, house systems, and languages.
    *   Responsive design.
    *   Displays generated SVG charts.
-   **API Endpoints**: Provides RESTful API for:
    *   Natal chart calculations.
    *   Chart visualizations (SVG).
-   **Extensible**: Designed for future expansion (e.g., synastry, composite charts, LLM interpretations).

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/zodiac-engine.git
cd zodiac-engine

# Create and activate virtual environment
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy the example below and save it as .env in the project root
```

## Configuration (`.env` File)

Create a `.env` file in the root directory of the project and add the following variables. Replace `"your_username"` with your actual GeoNames username.

```dotenv
PROJECT_NAME="Zodiac Engine API"
VERSION="1.0.0"
API_V1_STR="/api/v1"
ALLOWED_ORIGINS="http://localhost:8000,http://127.0.0.1:8000"

# Required for city/timezone lookup via GeoNames
# Create a free account at https://www.geonames.org/login
GEONAMES_USERNAME="your_username"
```

*Note: Ensure the `.env` file is saved with UTF-8 encoding and has correct formatting (no extra spaces around `=`).*

## Running the Application

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate # Or venv\Scripts\activate on Windows

# Run in development mode (with auto-reload)
uvicorn app.main:app --reload

# Run in production mode (example)
# uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Once running, access the:
-   **Web Interface**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
-   **API Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
-   **API Docs (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Test Scripts

The `scripts/` directory contains example shell scripts (`.sh`) for testing API endpoints using `curl`. These can be run from the project root after starting the application.

-   `scripts/test_western_chart.sh`: Generates a Western (Tropical) chart via API.
-   `scripts/test_vedic_chart.sh`: Generates a Vedic (Sidereal) chart via API.

```bash
# Example: Run the Western chart test script
bash scripts/test_western_chart.sh
```

## License

[MIT License](LICENSE)