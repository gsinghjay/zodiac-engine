"""Service for chart visualization using Kerykeion."""
import os
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from kerykeion import AstrologicalSubject, KerykeionChartSVG

from app.core.config import Settings
from app.schemas.chart_visualization import ChartConfiguration

# Get logger
logger = logging.getLogger(__name__)

# Define the directory where SVG images will be stored
SVG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                       "static", "images", "svg")

# Ensure the directory exists
os.makedirs(SVG_DIR, exist_ok=True)

# Map house system names to their corresponding Kerykeion identifiers
HOUSE_SYSTEM_MAP = {
    "Placidus": "P",
    "Koch": "K",
    "Whole Sign": "W",
    "Equal House": "A",  # Equal (Ascendant)
    "Equal (MC)": "E",
    "Campanus": "C",
    "Regiomontanus": "R",
    "Porphyry": "O",  # Porphyrius
    "Polich-Page Topocentric": "T",
    "Alcabitius": "B",
    "Morinus": "M",
    "Vehlow Equal": "V",
    "Axial Rotation": "X",
    "Horizon/Azimuth": "H"
}

def map_house_system(house_system: str) -> str:
    """
    Map a human-readable house system name to its Kerykeion identifier.
    
    Args:
        house_system: Human-readable house system name
        
    Returns:
        The single-letter Kerykeion identifier for the house system
    """
    if house_system in HOUSE_SYSTEM_MAP:
        return HOUSE_SYSTEM_MAP[house_system]
    
    # If it's already a valid single-letter identifier, return it
    if house_system in "ABCDEFGHIKLMNOPQRSTUVWXY":
        return house_system
    
    # Default to Placidus if not found
    logger.warning(f"Unknown house system '{house_system}', defaulting to Placidus (P)")
    return "P"

class ChartVisualizationService:
    """Service for generating and saving chart visualizations."""
    
    def __init__(self, settings: Settings):
        """Initialize the chart visualization service with settings."""
        self.settings = settings
    
    def generate_natal_chart_svg(
        self,
        name: str,
        birth_date: datetime,
        city: str | None = None,
        nation: str | None = None,
        lng: float | None = None,
        lat: float | None = None,
        tz_str: str | None = None,
        chart_id: str | None = None,
        theme: str = "dark",
        chart_language: str = "EN",
        config: dict[str, Any] | None = None,
    ) -> dict[str, str]:
        """
        Generate a natal chart SVG visualization using Kerykeion.
        
        Args:
            name: Name of the person
            birth_date: Birth date and time
            city: City of birth (optional)
            nation: Country of birth (optional)
            lng: Longitude of birth place (optional)
            lat: Latitude of birth place (optional)
            tz_str: Timezone string (optional)
            chart_id: Optional custom ID for the chart
            theme: Chart theme ("light", "dark", "dark-high-contrast", "classic")
            chart_language: Chart language (default: "EN")
            config: Chart configuration options
                - houses_system: House system identifier (default: "P" for Placidus)
                - zodiac_type: Zodiac type ("Tropic" or "Sidereal")
                - sidereal_mode: Sidereal mode (required if zodiac_type is "Sidereal")
                - perspective_type: Type of perspective ("Apparent Geocentric", "Heliocentric", "Topocentric", "True Geocentric")
                - active_points: List of active planets and points
                - active_aspects: List of active aspects with their orbs
            
        Returns:
            Dictionary with chart_id and svg_url
        """
        try:
            # Use either the provided config or the default configuration
            # If config is None, use all defaults from ChartConfiguration
            # If config is provided, it already contains defaults for any missing keys from the Pydantic model
            current_config = config if config is not None else ChartConfiguration().model_dump()
            
            # Extract configuration options
            original_house_system = current_config.get("houses_system", "P")
            houses_system = map_house_system(original_house_system)
            logger.info(f"Mapped house system from '{original_house_system}' to '{houses_system}'")
            
            # Convert language to uppercase
            chart_language = chart_language.upper()
            logger.info(f"Using chart language: {chart_language}")
            
            zodiac_type = current_config.get("zodiac_type")
            sidereal_mode = current_config.get("sidereal_mode")
            perspective_type = current_config.get("perspective_type")
            active_points = current_config.get("active_points")
            active_aspects = current_config.get("active_aspects")
            
            # Generate a unique ID if not provided
            if not chart_id:
                chart_id = f"natal_{uuid.uuid4().hex[:8]}"
                
            # Define the SVG file path
            svg_path = os.path.join(SVG_DIR, f"{chart_id}.svg")
            svg_path_obj = Path(svg_path)
            
            # Create the AstrologicalSubject with zodiac and house configuration
            subject = AstrologicalSubject(
                name=name,
                year=birth_date.year,
                month=birth_date.month,
                day=birth_date.day,
                hour=birth_date.hour,
                minute=birth_date.minute,
                city=city,
                nation=nation,
                lng=lng,
                lat=lat,
                tz_str=tz_str,
                houses_system_identifier=houses_system,
                zodiac_type=zodiac_type,
                sidereal_mode=sidereal_mode,
                perspective_type=perspective_type,
                geonames_username=self.settings.GEONAMES_USERNAME,
                online=bool(self.settings.GEONAMES_USERNAME)  # Use online mode when username is provided
            )
            
            # Generate the SVG chart with custom output directory and configuration
            chart = KerykeionChartSVG(
                subject, 
                chart_type='Natal',
                theme=theme,
                chart_language=chart_language,
                new_output_directory=str(Path(SVG_DIR)),
                active_points=active_points,
                active_aspects=active_aspects
            )
            
            # Save the chart with a custom filename
            # First create the chart's template
            chart.template = chart.makeTemplate()
            
            # Write to custom path (overriding default behavior)
            with open(svg_path, "w", encoding="utf-8", errors="ignore") as output_file:
                output_file.write(chart.template)
            
            logger.info(f"Chart saved as {svg_path}")
            
            # Return the chart ID and URL
            return {
                "chart_id": chart_id,
                "svg_url": f"/static/images/svg/{chart_id}.svg"
            }
            
        except Exception as e:
            logger.error(f"Error generating chart visualization: {str(e)}", exc_info=True)
            raise
    
    def generate_synastry_chart_svg(
        self,
        name1: str,
        birth_date1: datetime,
        name2: str,
        birth_date2: datetime,
        city1: str | None = None,
        nation1: str | None = None,
        lng1: float | None = None,
        lat1: float | None = None,
        tz_str1: str | None = None,
        city2: str | None = None,
        nation2: str | None = None,
        lng2: float | None = None,
        lat2: float | None = None,
        tz_str2: str | None = None,
        chart_id: str | None = None,
        theme: str = "dark",
        chart_language: str = "EN",
        config: dict[str, Any] | None = None,
    ) -> dict[str, str]:
        """
        Generate a synastry chart SVG visualization using Kerykeion.
        
        Args:
            name1: Name of the first person
            birth_date1: Birth date and time of the first person
            name2: Name of the second person
            birth_date2: Birth date and time of the second person
            city1, nation1, lng1, lat1, tz_str1: Location data for first person
            city2, nation2, lng2, lat2, tz_str2: Location data for second person
            chart_id: Optional custom ID for the chart
            theme: Chart theme ("light", "dark", "dark-high-contrast", "classic")
            chart_language: Chart language (default: "EN")
            config: Chart configuration options
                - houses_system: House system identifier (default: "P" for Placidus)
                - zodiac_type: Zodiac type ("Tropic" or "Sidereal")
                - sidereal_mode: Sidereal mode (required if zodiac_type is "Sidereal")
                - perspective_type: Type of perspective ("Apparent Geocentric", "Heliocentric", "Topocentric", "True Geocentric")
                - active_points: List of active planets and points
                - active_aspects: List of active aspects with their orbs
            
        Returns:
            Dictionary with chart_id and svg_url
        """
        try:
            # Use either the provided config or the default configuration
            # If config is None, use all defaults from ChartConfiguration
            # If config is provided, it already contains defaults for any missing keys from the Pydantic model
            current_config = config if config is not None else ChartConfiguration().model_dump()
            
            # Extract configuration options
            original_house_system = current_config.get("houses_system", "P")
            houses_system = map_house_system(original_house_system)
            logger.info(f"Mapped house system from '{original_house_system}' to '{houses_system}'")
            
            # Convert language to uppercase
            chart_language = chart_language.upper()
            logger.info(f"Using chart language: {chart_language}")
            
            zodiac_type = current_config.get("zodiac_type")
            sidereal_mode = current_config.get("sidereal_mode")
            perspective_type = current_config.get("perspective_type")
            active_points = current_config.get("active_points")
            active_aspects = current_config.get("active_aspects")
            
            # Generate a unique ID if not provided
            if not chart_id:
                chart_id = f"synastry_{uuid.uuid4().hex[:8]}"
                
            # Define the SVG file path
            svg_path = os.path.join(SVG_DIR, f"{chart_id}.svg")
            svg_path_obj = Path(svg_path)
            
            # Create the first AstrologicalSubject with zodiac and house configuration
            subject1 = AstrologicalSubject(
                name=name1,
                year=birth_date1.year,
                month=birth_date1.month,
                day=birth_date1.day,
                hour=birth_date1.hour,
                minute=birth_date1.minute,
                city=city1,
                nation=nation1,
                lng=lng1,
                lat=lat1,
                tz_str=tz_str1,
                houses_system_identifier=houses_system,
                zodiac_type=zodiac_type,
                sidereal_mode=sidereal_mode,
                perspective_type=perspective_type,
                geonames_username=self.settings.GEONAMES_USERNAME,
                online=bool(self.settings.GEONAMES_USERNAME)  # Use online mode when username is provided
            )
            
            # Create the second AstrologicalSubject with zodiac and house configuration
            subject2 = AstrologicalSubject(
                name=name2,
                year=birth_date2.year,
                month=birth_date2.month,
                day=birth_date2.day,
                hour=birth_date2.hour,
                minute=birth_date2.minute,
                city=city2,
                nation=nation2,
                lng=lng2,
                lat=lat2,
                tz_str=tz_str2,
                houses_system_identifier=houses_system,
                zodiac_type=zodiac_type,
                sidereal_mode=sidereal_mode,
                perspective_type=perspective_type,
                geonames_username=self.settings.GEONAMES_USERNAME,
                online=bool(self.settings.GEONAMES_USERNAME)  # Use online mode when username is provided
            )
            
            # Generate the SVG chart with custom output directory and configuration
            chart = KerykeionChartSVG(
                subject1, 
                chart_type='Synastry',
                second_obj=subject2,
                theme=theme,
                chart_language=chart_language,
                new_output_directory=str(Path(SVG_DIR)),
                active_points=active_points,
                active_aspects=active_aspects
            )
            
            # Save the chart with a custom filename
            # First create the chart's template
            chart.template = chart.makeTemplate()
            
            # Write to custom path (overriding default behavior)
            with open(svg_path, "w", encoding="utf-8", errors="ignore") as output_file:
                output_file.write(chart.template)
            
            logger.info(f"Synastry chart saved as {svg_path}")
            
            # Return the chart ID and URL
            return {
                "chart_id": chart_id,
                "svg_url": f"/static/images/svg/{chart_id}.svg"
            }
            
        except Exception as e:
            logger.error(f"Error generating synastry chart visualization: {str(e)}", exc_info=True)
            raise 