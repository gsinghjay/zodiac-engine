#!/bin/bash

# Test script to generate Western (Tropical) natal chart using curl

#=================================================
# CONFIGURATION VARIABLES - Modify as needed
#=================================================

# API Base URL
BASE_URL="http://localhost:8000"

# Birth data 
NAME="Jay Singh"
BIRTH_DATE="1994-07-17T10:30:00"
CITY="Queens"
NATION="US"
LNG=-73.8667  # 73w52 in decimal format
LAT=40.7167   # 40n43 in decimal format
TZ_STR="America/New_York"  # Timezone for New York

# Chart visualization options
CHART_THEME="light"        # Options: dark, light, classic, dark-high-contrast
CHART_LANGUAGE="EN"       # Options: EN, FR, PT, IT, CN, ES, RU, TR, DE, HI
HOUSES_SYSTEM="P"         # Options: P (Placidus), W (Whole Sign), K (Koch), etc.
ZODIAC_TYPE="Tropic"      # Options: Tropic, Sidereal
SIDEREAL_MODE=""          # Not needed for Tropical zodiac
PERSPECTIVE="Apparent Geocentric"  # Options: Apparent Geocentric, Heliocentric, Topocentric, True Geocentric

# Active points to include in the chart - include ALL available points for comprehensive Western chart
ACTIVE_POINTS=(
  # Traditional planets
  "Sun" "Moon" "Mercury" "Venus" "Mars" "Jupiter" "Saturn"
  # Modern planets
  "Uranus" "Neptune" "Pluto" 
  # Angles and axes
  "Ascendant" "Medium_Coeli" "Descendant" "Imum_Coeli"
  # Additional points important in Western astrology 
  "Chiron" "Mean_Node" "True_Node" "Mean_South_Node" "True_South_Node" "Mean_Lilith"
)

# Note: The following Western astrological elements are commonly used but not yet supported by our API:
# - Asteroids (Ceres, Pallas, Juno, Vesta)
# - Part of Fortune and other Arabic Parts
# - Fixed Stars (Regulus, Spica, Algol, etc.)
# - Planetary Midpoints
# - Declination values and Out-of-Bounds planets
# - Harmonics and Composite charts

# Aspects to include with orbs - Western astrology typically uses more aspects
declare -A ASPECTS
ASPECTS["conjunction"]=8
ASPECTS["opposition"]=8
ASPECTS["trine"]=7
ASPECTS["square"]=7
ASPECTS["sextile"]=6
ASPECTS["semi-sextile"]=3
ASPECTS["semi-square"]=3
ASPECTS["sesquiquadrate"]=3
ASPECTS["quincunx"]=3
ASPECTS["quintile"]=2
ASPECTS["biquintile"]=2

#=================================================
# SCRIPT EXECUTION - No need to modify below
#=================================================

echo "Testing Western Chart Generation API..."
echo "======================================"

# Format active points array as JSON array
ACTIVE_POINTS_JSON=$(printf '"%s", ' "${ACTIVE_POINTS[@]}" | sed 's/, $//')
ACTIVE_POINTS_JSON="[${ACTIVE_POINTS_JSON}]"

# Format aspects as JSON array
ASPECTS_JSON=""
for aspect in "${!ASPECTS[@]}"; do
  ASPECTS_JSON+="{ \"name\": \"$aspect\", \"orb\": ${ASPECTS[$aspect]} }, "
done
ASPECTS_JSON=$(echo "$ASPECTS_JSON" | sed 's/, $//')
ASPECTS_JSON="[${ASPECTS_JSON}]"

# Build config JSON
CONFIG_JSON="{"
CONFIG_JSON+="\"houses_system\": \"${HOUSES_SYSTEM}\", "
CONFIG_JSON+="\"zodiac_type\": \"${ZODIAC_TYPE}\", "
CONFIG_JSON+="\"perspective_type\": \"${PERSPECTIVE}\", "
CONFIG_JSON+="\"active_points\": ${ACTIVE_POINTS_JSON}, "
CONFIG_JSON+="\"active_aspects\": ${ASPECTS_JSON}"
# Add sidereal mode if provided
if [ ! -z "$SIDEREAL_MODE" ]; then
  CONFIG_JSON+=", \"sidereal_mode\": \"${SIDEREAL_MODE}\""
fi
CONFIG_JSON+="}"

# 1. Generate basic natal chart
echo "Generating basic natal chart..."
curl -s -X POST \
  "${BASE_URL}/api/v1/charts/natal/" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${NAME}\",
    \"birth_date\": \"${BIRTH_DATE}\",
    \"city\": \"${CITY}\",
    \"nation\": \"${NATION}\",
    \"lng\": ${LNG},
    \"lat\": ${LAT},
    \"tz_str\": \"${TZ_STR}\",
    \"houses_system\": \"${HOUSES_SYSTEM}\"
  }" | jq '.' || echo "Failed to parse JSON. Raw response:"

echo -e "\n\n"

# 2. Generate natal chart visualization
echo "Generating natal chart visualization..."
CHART_ID="jay_western_$(date +%s)"
curl -s -X POST \
  "${BASE_URL}/api/v1/charts/visualization/natal" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${NAME}\",
    \"birth_date\": \"${BIRTH_DATE}\",
    \"city\": \"${CITY}\",
    \"nation\": \"${NATION}\",
    \"lng\": ${LNG},
    \"lat\": ${LAT},
    \"tz_str\": \"${TZ_STR}\",
    \"chart_id\": \"${CHART_ID}\",
    \"theme\": \"${CHART_THEME}\",
    \"language\": \"${CHART_LANGUAGE}\",
    \"config\": ${CONFIG_JSON}
  }" | jq '.' || echo "Failed to parse JSON. Raw response:"

echo -e "\n"
echo "Chart ID: ${CHART_ID}"
echo "Chart should be available at: ${BASE_URL}/static/images/svg/${CHART_ID}.svg"
echo "To view the chart, open a browser and navigate to the URL above"
echo -e "\n"

echo "Done!" 