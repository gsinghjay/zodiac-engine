# Zodiac Engine API Test Scripts

This directory contains Bash scripts designed to test the natal chart generation capabilities of the Zodiac Engine API. There are two scripts, one configured for Vedic (Sidereal) astrology standards and the other for Western (Tropical) astrology standards.

Both scripts use the same birth data to allow for easy comparison between the two astrological systems.

## Prerequisites

Before running these scripts, ensure that:

1.  The Zodiac Engine API server is running locally.
2.  The API is accessible at `http://localhost:8000` (you can change the `BASE_URL` variable in the scripts if needed).
3.  `curl` and `jq` command-line tools are installed on your system.
    - `curl` is used to make HTTP requests to the API.
    - `jq` is used to format the JSON responses for better readability.

## Scripts

### 1. `test_vedic_chart.sh`

**Purpose:** This script tests the API's natal chart generation using settings commonly associated with Vedic (Indian) astrology.

**Key Configurations:**

*   **Zodiac Type:** `Sidereal` - Uses the sidereal zodiac, which accounts for the precession of the equinoxes.
*   **Sidereal Mode:** `LAHIRI` - Employs the Lahiri ayanamsa, the most widely accepted ayanamsa in India.
*   **House System:** `W` (Whole Sign) - A traditional house system frequently used in Vedic astrology where each house occupies one full sign.
*   **Active Points:** Includes a comprehensive set of points relevant in Vedic analysis, such as both Mean and True Nodes.
*   **Aspects:** Configured with orbs commonly used in Vedic practice (e.g., wider orbs for major aspects like conjunctions and oppositions).
*   **Theme:** `classic` - For a traditional chart appearance.

**How it was Formulated:**
The settings were chosen based on standard Vedic astrological practices. The LAHIRI ayanamsa and Whole Sign houses are defaults in many Vedic software applications. The included points and aspect orbs reflect common usage within the Vedic community.

**How to Run:**

```bash
chmod +x test_vedic_chart.sh
./test_vedic_chart.sh
```

### 2. `test_western_chart.sh`

**Purpose:** This script tests the API's natal chart generation using settings commonly associated with modern Western astrology.

**Key Configurations:**

*   **Zodiac Type:** `Tropic` - Uses the tropical zodiac, which is standard in Western astrology.
*   **House System:** `P` (Placidus) - The most widely used house system in modern Western astrology.
*   **Active Points:** Includes standard Western points: Sun through Pluto, major angles (Asc, MC, Desc, IC), Chiron, Mean Node, and Mean Lilith.
*   **Aspects:** Includes a broader range of major and minor aspects with orbs typically used in Western practice.
*   **Theme:** `light` - For a modern chart appearance.

**How it was Formulated:**
The settings reflect contemporary Western astrological standards. The Tropical zodiac and Placidus houses are the most common defaults. The included points and aspects cover the core elements analyzed by most Western astrologers.

**How to Run:**

```bash
chmod +x test_western_chart.sh
./test_western_chart.sh
```

## Output

Both scripts perform two main actions:

1.  **Generate Basic Natal Chart Data:** Makes a `POST` request to `/api/v1/charts/natal/` and prints the resulting JSON data (planetary positions, house cusps, aspects) formatted by `jq`.
2.  **Generate Natal Chart Visualization:** Makes a `POST` request to `/api/v1/charts/visualization/natal` with the specified configurations. It prints the JSON response containing the `chart_id` and `svg_url`.

The script also outputs the full URL where the generated SVG chart image *should* be accessible if the API server is configured correctly to serve static files from the `app/static/images/svg/` directory.

**Note on Missing Features:**
While these scripts test the core natal chart functionality, they also highlight features common in each system that are *not yet implemented* in the underlying Kerykeion library or our API wrapper. These include:

*   **Vedic:** Dasha systems (planetary periods), Divisional Charts (like Navamsa D-9), detailed Dosha analysis, Ashtakvarga.
*   **Western:** Major Asteroids (Ceres, Pallas, Juno, Vesta), Part of Fortune, Fixed Stars, Midpoints, Declination. 