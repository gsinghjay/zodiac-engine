#!/bin/bash

# Test script to generate Vedic (Sidereal) natal chart using curl

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
CHART_THEME="classic"        # Options: dark, light, classic, dark-high-contrast
CHART_LANGUAGE="EN"       # Options: EN, FR, PT, IT, CN, ES, RU, TR, DE, HI
HOUSES_SYSTEM="W"         # Options: P (Placidus), W (Whole Sign), K (Koch), etc.
ZODIAC_TYPE="Sidereal"      # Options: Tropic, Sidereal
SIDEREAL_MODE="LAHIRI"          # Required if ZODIAC_TYPE="Sidereal", e.g., "FAGAN_BRADLEY"
PERSPECTIVE="Apparent Geocentric"  # Options: Apparent Geocentric, Heliocentric, etc.

# Active points to include in the chart - include ALL available points for comprehensive Vedic chart
ACTIVE_POINTS=(
  "Sun" "Moon" "Mercury" "Venus" "Mars" "Jupiter" "Saturn"
  "Uranus" "Neptune" "Pluto" "Ascendant" "Medium_Coeli" "Descendant" "Imum_Coeli"
  "Mean_Node" "True_Node" "Mean_South_Node" "True_South_Node" "Chiron" "Mean_Lilith"
)

# Aspects to include with orbs - Vedic astrology typically focuses on specific aspects
declare -A ASPECTS
ASPECTS["conjunction"]=10
ASPECTS["opposition"]=10
ASPECTS["trine"]=8
ASPECTS["square"]=8
ASPECTS["sextile"]=6
# Less commonly used in Vedic but still valuable
ASPECTS["quincunx"]=3
ASPECTS["semi-sextile"]=2
ASPECTS["quintile"]=2

#=================================================
# SCRIPT EXECUTION - No need to modify below
#=================================================

echo "Testing Vedic Chart Generation API..."
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
CHART_ID="jay_vedic_$(date +%s)"
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