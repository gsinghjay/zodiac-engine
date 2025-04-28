# Zodiac Engine

A modern astrological calculation API powered by [Kerykeion](https://github.com/giacomobattista/kerykeion) library.

## Features

- ✅ Natal Chart Calculations
- ✅ Synastry Analysis
- ✅ Composite Charts
- ✅ Transit Calculations
- ✅ SVG Chart Visualizations
- 🚧 LLM-powered Interpretations (Coming Soon)

## Installation

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) (optional, for development)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/zodiac-engine.git
   cd zodiac-engine
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Environment Variables:
   
   Create a `.env` file in the project root with the following variables:
   ```
   # Application settings
   PROJECT_NAME="Zodiac Engine API"  # The name of the project displayed in API docs
   VERSION="1.0.0"                   # API version for documentation
   API_V1_STR="/api/v1"              # API version prefix for all endpoints
   ALLOWED_ORIGINS="*"               # Comma-separated list of allowed CORS origins
   
   # Kerykeion settings
   GEONAMES_USERNAME=""              # Username for GeoNames API (optional)
   ```
   
   The `GEONAMES_USERNAME` is optional but recommended for enhanced geolocation features.
   You can obtain a free username by registering at [GeoNames](https://www.geonames.org/login).
   
   For CORS configuration, you can specify multiple origins using commas:
   ```
   ALLOWED_ORIGINS="http://localhost:3000,https://yourdomain.com"
   ```

## Usage

Run the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access:

- Interactive API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

## API Endpoints

### Natal Charts

```
POST /api/v1/charts/natal/
```

Calculate a complete natal chart based on birth data.

**Example Request:**

```json
{
  "name": "John Doe",
  "birth_date": "1990-01-01T12:00:00",
  "city": "New York",
  "nation": "US",
  "lng": -74.006,
  "lat": 40.7128,
  "tz_str": "America/New_York"
}
```

### Other Chart Types

- Synastry: `POST /api/v1/charts/synastry/`
- Composite: `POST /api/v1/charts/composite/`
- Transit: `POST /api/v1/charts/transit/`

### SVG Chart Visualizations

```
POST /api/v1/charts/visualization/natal
POST /api/v1/charts/visualization/synastry
```

Generate SVG visualizations of natal and synastry charts with customizable options.

```
GET /static/images/svg/{chart_id}.svg
```

Retrieves an SVG visualization of a chart by its ID.

#### Chart Customization Options

Charts can be customized with the following configuration options:

```json
{
  "config": {
    "zodiac_type": "Tropic",           // "Tropic" or "Sidereal"
    "sidereal_mode": "FAGAN_BRADLEY",  // Required when zodiac_type is "Sidereal"
    "houses_system": "P",              // House system identifier (e.g., "P" for Placidus, "K" for Koch)
    "perspective_type": "Apparent Geocentric", // "Apparent Geocentric", "True Geocentric", "Heliocentric", "Topocentric"
    "active_points": [                 // Celestial bodies and points to include in the chart
      "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", 
      "Uranus", "Neptune", "Pluto", "Mean_Node", "Chiron", 
      "Ascendant", "Medium_Coeli"
    ],
    "active_aspects": [                // Aspects to calculate and display
      {"name": "conjunction", "orb": 10},
      {"name": "opposition", "orb": 10},
      {"name": "trine", "orb": 8},
      {"name": "sextile", "orb": 6},
      {"name": "square", "orb": 5}
    ]
  },
  "theme": "classic",                  // Chart theme: "classic", "light", "dark", "dark-high-contrast"
  "language": "EN"                     // Chart language: "EN", "FR", "PT", "IT", "CN", "ES", "RU", "TR", "DE", "HI"
}
```

**Example Request:**

```json
{
  "name": "John Doe",
  "birth_date": "1990-01-01T12:00:00",
  "city": "New York",
  "nation": "US",
  "language": "EN",
  "theme": "dark",
  "config": {
    "zodiac_type": "Sidereal",
    "sidereal_mode": "FAGAN_BRADLEY",
    "houses_system": "K",
    "perspective_type": "Apparent Geocentric",
    "active_points": ["Sun", "Moon", "Ascendant", "Medium_Coeli"],
    "active_aspects": [
      {"name": "conjunction", "orb": 8},
      {"name": "opposition", "orb": 8}
    ]
  }
}
```

## Project Structure

```
zodiac-engine/
├── app/                    # Application package
│   ├── api/                # API endpoints
│   │   └── v1/             # Version 1 API
│   │       └── routers/    # API router modules
│   │           └── charts/ # Chart routers
│   ├── core/               # Core functionality
│   │   ├── config.py       # Application settings
│   │   └── dependencies.py # Dependency injection
│   ├── schemas/            # Pydantic models
│   ├── services/           # Business logic
│   ├── static/             # Static files
│   │   └── images/         # Image files
│   │       └── svg/        # SVG chart visualizations
│   └── main.py             # FastAPI application
├── tests/                  # Test package
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## Development

### Setting Up Development Environment

```bash
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_static_images.py

# Run a specific test function
pytest tests/test_static_images.py::test_generate_natal_chart_visualization
```

#### Viewing Generated SVG Files

When running individual tests that generate SVG files, the files are created in the `app/static/images/svg/` directory. For example:

```bash
# Run a test that generates an SVG file
pytest tests/test_static_images.py::test_generate_natal_chart_visualization -v

# View the generated SVG file
# On Linux/macOS
open app/static/images/svg/test_natal_chart.svg

# On Windows
start app/static/images/svg/test_natal_chart.svg
```

Note: When running the full test suite, SVG files are automatically cleaned up after all tests complete, except for `sample.svg`. If you want to examine generated SVGs, run individual test cases instead.

### FastAPI Best Practices

This project follows modern FastAPI best practices:

- **Pydantic v2**: Using modern syntax (`| None` instead of `Optional[]`, etc.)
- **Dependency Injection**: Services are injected using FastAPI's DI system
- **Environment Configuration**: Settings class with proper .env integration
- **Response Models**: Properly typed response models for all endpoints
- **Status Codes**: Using FastAPI status constants for consistency
- **CORS Configuration**: Robust handling of allowed origins

### Code Style

This project follows:
- SOLID principles
- DRY (Don't Repeat Yourself)
- Conventional commits
- Type hints throughout the codebase

## Roadmap

View our development roadmap in [docs/kerykeion/task-natal-chart.md](docs/kerykeion/task-natal-chart.md).

## License

MIT License 