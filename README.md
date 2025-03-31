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
GET /static/images/charts/{chart_id}
```

Retrieves an SVG visualization of a chart by its ID.

## Project Structure

```
zodiac-engine/
├── app/                    # Application package
│   ├── api/                # API endpoints
│   │   └── v1/             # Version 1 API
│   │       └── endpoints/  # API endpoint modules
│   │           └── charts/ # Chart endpoints
│   ├── core/               # Core functionality
│   ├── routers/            # Router modules
│   │   └── static/         # Static files router
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