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
   PROJECT_NAME="Zodiac Engine API"
   VERSION="1.0.0"
   API_V1_STR="/api/v1"
   ALLOWED_ORIGINS="*"
   
   # Kerykeion settings
   GEONAMES_USERNAME=""
   ```
   
   The `GEONAMES_USERNAME` is optional but recommended for enhanced geolocation features.
   You can obtain a free username by registering at [GeoNames](https://www.geonames.org/login).

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
│   │       └── endpoints/  # API endpoint modules
│   │           └── charts/ # Chart endpoints
│   ├── core/               # Core functionality
│   ├── static/             # Static files
│   │   └── images/         # Image files
│   │       └── svg/        # SVG chart visualizations
│   ├── schemas/            # Pydantic models
│   ├── services/           # Business logic
│   └── main.py             # FastAPI application
├── tests/                  # Test package
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
pytest
```

### Code Style

This project follows PEP 8 guidelines and uses:
- SOLID principles
- DRY (Don't Repeat Yourself)
- Conventional commits

## Roadmap

View our development roadmap in [docs/kerykeion/task-natal-chart.md](docs/kerykeion/task-natal-chart.md).

## License

MIT License 