"""Service for chart visualization using Kerykeion."""
import os
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Union

from kerykeion import AstrologicalSubject, KerykeionChartSVG

# Get logger
logger = logging.getLogger(__name__)

# Define the directory where SVG images will be stored
SVG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                       "static", "images", "svg")

# Ensure the directory exists
os.makedirs(SVG_DIR, exist_ok=True)

class ChartVisualizationService:
    """Service for generating and saving chart visualizations."""
    
    @staticmethod
    def generate_natal_chart_svg(
        name: str,
        birth_date: datetime,
        city: Optional[str] = None,
        nation: Optional[str] = None,
        lng: Optional[float] = None,
        lat: Optional[float] = None,
        tz_str: Optional[str] = None,
        houses_system: str = "P",
        theme: str = "dark",
        chart_language: str = "EN",
        chart_id: Optional[str] = None
    ) -> Dict[str, str]:
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
            houses_system: House system identifier (default: "P" for Placidus)
            theme: Chart theme ("light", "dark", "dark-high-contrast", "classic")
            chart_language: Chart language (default: "EN")
            chart_id: Optional custom ID for the chart
            
        Returns:
            Dictionary with chart_id and svg_url
        """
        try:
            # Generate a unique ID if not provided
            if not chart_id:
                chart_id = f"natal_{uuid.uuid4().hex[:8]}"
                
            # Define the SVG file path
            svg_path = os.path.join(SVG_DIR, f"{chart_id}.svg")
            svg_path_obj = Path(svg_path)
            
            # Create the AstrologicalSubject
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
            )
            
            # Generate the SVG chart with custom output directory
            chart = KerykeionChartSVG(
                subject, 
                chart_type='Natal',
                theme=theme,
                chart_language=chart_language,
                new_output_directory=str(Path(SVG_DIR))
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
    
    @staticmethod
    def generate_synastry_chart_svg(
        name1: str,
        birth_date1: datetime,
        name2: str,
        birth_date2: datetime,
        city1: Optional[str] = None,
        nation1: Optional[str] = None,
        lng1: Optional[float] = None,
        lat1: Optional[float] = None,
        tz_str1: Optional[str] = None,
        city2: Optional[str] = None,
        nation2: Optional[str] = None,
        lng2: Optional[float] = None,
        lat2: Optional[float] = None,
        tz_str2: Optional[str] = None,
        houses_system: str = "P",
        theme: str = "dark",
        chart_language: str = "EN",
        chart_id: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate a synastry chart SVG visualization using Kerykeion.
        
        Args:
            name1: Name of the first person
            birth_date1: Birth date and time of the first person
            name2: Name of the second person
            birth_date2: Birth date and time of the second person
            city1, nation1, lng1, lat1, tz_str1: Location data for first person
            city2, nation2, lng2, lat2, tz_str2: Location data for second person
            houses_system: House system identifier (default: "P" for Placidus)
            theme: Chart theme ("light", "dark", "dark-high-contrast", "classic")
            chart_language: Chart language (default: "EN")
            chart_id: Optional custom ID for the chart
            
        Returns:
            Dictionary with chart_id and svg_url
        """
        try:
            # Generate a unique ID if not provided
            if not chart_id:
                chart_id = f"synastry_{uuid.uuid4().hex[:8]}"
                
            # Define the SVG file path
            svg_path = os.path.join(SVG_DIR, f"{chart_id}.svg")
            svg_path_obj = Path(svg_path)
            
            # Create the first AstrologicalSubject
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
            )
            
            # Create the second AstrologicalSubject
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
            )
            
            # Generate the SVG chart with custom output directory
            chart = KerykeionChartSVG(
                subject1, 
                chart_type='Synastry',
                second_obj=subject2,
                theme=theme,
                chart_language=chart_language,
                new_output_directory=str(Path(SVG_DIR))
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