# Product Context: Zodiac Engine

## 1. Problem Statement

Developers and astrologers often need reliable, programmatic access to astrological calculations and visualizations. Building these features from scratch is complex, time-consuming, and requires deep astrological knowledge combined with software expertise. Existing tools might be outdated, lack modern API interfaces, or be difficult to integrate.

## 2. Solution

Zodiac Engine provides a modern FastAPI-based API that wraps the powerful Kerykeion library. It offers:
- **Easy Integration**: A standard REST API for seamless integration into various applications.
- **Accurate Calculations**: Leverages the well-tested Kerykeion library for reliable astrological data.
- **Customizable Visualizations**: Generates SVG charts with options for themes, languages, points, and aspects.
- **Developer Focus**: Built with modern Python practices, making it easy for developers to use and extend.

## 3. How it Works

- Users send HTTP requests (POST) to specific API endpoints (e.g., `/api/v1/charts/natal`, `/api/v1/charts/visualization/natal`).
- Requests include necessary data (birth details, location, configuration options) defined by Pydantic schemas.
- The API backend uses the `AstrologyService` and `ChartVisualizationService` to interact with the Kerykeion library.
- Services perform calculations or generate SVG charts.
- The API returns JSON responses with calculated data or SVG URLs.
- SVG charts are stored statically and served via a dedicated endpoint.

## 4. User Experience Goals

- **Developer Experience (DX)**: Simple, intuitive API design; clear documentation (OpenAPI); easy setup and deployment.
- **Reliability**: Consistent and accurate results.
- **Performance**: Reasonably fast response times for calculations and visualizations.
- **Flexibility**: Sufficient configuration options to meet common use cases for chart generation. 