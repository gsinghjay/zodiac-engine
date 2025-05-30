"""Service for generating astrological reports using Kerykeion's Report class."""
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from kerykeion import AstrologicalSubject, Report
from app.services.chart_visualization import map_house_system

logger = logging.getLogger(__name__)

class ReportGenerationError(Exception):
    """Exception raised when report generation fails."""
    pass

class ReportService:
    """Service for generating astrological reports from chart data."""

    def __init__(self):
        """Initialize the report service."""
        pass

    def generate_natal_report(
        self, 
        name: str, 
        birth_date: datetime,
        birth_place: str,
        lat: float,
        lng: float,
        house_system: Optional[str] = "Placidus",
        timezone: Optional[str] = None
    ) -> Dict[str, str]:
        """Generate a report for a natal chart.
        
        Args:
            name: The name of the person
            birth_date: The birth date and time
            birth_place: The birth place name
            lat: The latitude of the birth place
            lng: The longitude of the birth place
            house_system: The house system to use (default: Placidus)
            timezone: The timezone of the birth place
            
        Returns:
            Dict[str, str]: Dictionary with report components matching NatalReportResponse
        """
        try:
            # Log the inputs
            logger.info(f"Generating natal report for {name} born on {birth_date}")
            
            # Map the house system if needed
            mapped_house_system = self._map_house_system(house_system)
            logger.debug(f"Mapped house system from '{house_system}' to '{mapped_house_system}'")
            
            # Set a default timezone if none provided
            if not timezone:
                logger.warning("No timezone provided for natal report, defaulting to UTC")
                timezone = "UTC"
                
            # Create AstrologicalSubject instance
            year = birth_date.year
            month = birth_date.month
            day = birth_date.day
            hour = birth_date.hour
            minute = birth_date.minute
            
            # Extract country code from birth_place if possible
            # Format expected: "City, CountryCode"
            country_code = "US"  # Default
            if "," in birth_place:
                country_code = birth_place.split(",")[1].strip()
                birth_place = birth_place.split(",")[0].strip()
                
            logger.debug(f"Creating AstrologicalSubject with: {name}, {year}, {month}, {day}, {hour}, {minute}, {birth_place}, {country_code}, lng={lng}, lat={lat}")
            subject = AstrologicalSubject(
                name=name,
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                city=birth_place,
                nation=country_code,
                lng=lng,
                lat=lat,
                houses_system_identifier=mapped_house_system,
                tz_str=timezone
            )
            
            logger.debug("Created AstrologicalSubject successfully")
            
            # Generate report
            report = Report(subject)
            full_report = report.get_full_report()
            
            # If using Whole Sign houses, add a note explaining the positions
            if mapped_house_system == "W":
                note = "\nNote: For Whole Sign houses, all house positions are 0.0 as each house starts at 0° of its sign.\n"
                full_report += note
                
            # Extract components from report
            report_parts = full_report.split('\n')
            
            # Title is the first line
            title = report_parts[0].strip() if report_parts else f"Kerykeion report for {name}"
            
            # Find the table boundaries using the ASCII table markers
            data_table_start = full_report.find("+-----------+")
            data_table_end = full_report.find("+-----------------+------+")
            
            planets_table_start = data_table_end
            planets_table_end = full_report.find("+----------------+------+")
            
            houses_table_start = planets_table_end
            houses_table_end = full_report.find("Note: For Whole Sign") if "Note: For Whole Sign" in full_report else len(full_report)
            
            # Extract the tables
            data_table = full_report[data_table_start:data_table_end].strip()
            planets_table = full_report[planets_table_start:planets_table_end].strip()
            houses_table = full_report[houses_table_start:houses_table_end].strip()
            
            # Return structured data matching NatalReportResponse
            logger.info("Successfully generated natal report")
            return {
                "title": title,
                "data_table": data_table,
                "planets_table": planets_table,
                "houses_table": houses_table,
                "full_report": full_report
            }
            
        except Exception as e:
            logger.error(f"Error generating natal report: {str(e)}")
            raise ReportGenerationError(f"Failed to generate natal report: {str(e)}")

    def generate_synastry_report(
        self, 
        person1_name: str, 
        person1_birth_date: datetime,
        person1_birth_place: str,
        person1_lat: float,
        person1_lng: float,
        person2_name: str, 
        person2_birth_date: datetime,
        person2_birth_place: str,
        person2_lat: float,
        person2_lng: float,
        house_system: Optional[str] = "Placidus",
        timezone: Optional[str] = None
    ) -> Dict[str, Dict[str, str]]:
        """Generate a synastry report comparing two natal charts.
        
        Args:
            person1_name, person2_name: Names of the individuals
            person1_birth_date, person2_birth_date: Birth dates and times
            person1_birth_place, person2_birth_place: Birth places 
            person1_lat, person1_lng: Coordinates for person 1
            person2_lat, person2_lng: Coordinates for person 2
            house_system: House system to use
            timezone: Timezone for the charts
            
        Returns:
            Dict[str, Dict[str, str]]: Dictionary with person1 and person2 report data
        """
        try:
            # Log the inputs
            logger.info(f"Generating synastry report for {person1_name} and {person2_name}")
            
            # Map the house system if needed
            mapped_house_system = self._map_house_system(house_system)
            
            # Set a default timezone if none provided
            if not timezone:
                logger.warning("No timezone provided for synastry report, defaulting to UTC")
                timezone = "UTC"
                
            # Create first AstrologicalSubject
            person1 = AstrologicalSubject(
                name=person1_name,
                year=person1_birth_date.year,
                month=person1_birth_date.month,
                day=person1_birth_date.day,
                hour=person1_birth_date.hour,
                minute=person1_birth_date.minute,
                city=person1_birth_place.split(",")[0].strip() if "," in person1_birth_place else person1_birth_place,
                nation=person1_birth_place.split(",")[1].strip() if "," in person1_birth_place else "US",
                lng=person1_lng,
                lat=person1_lat,
                houses_system_identifier=mapped_house_system,
                tz_str=timezone
            )
            
            # Create second AstrologicalSubject
            person2 = AstrologicalSubject(
                name=person2_name,
                year=person2_birth_date.year,
                month=person2_birth_date.month,
                day=person2_birth_date.day,
                hour=person2_birth_date.hour,
                minute=person2_birth_date.minute,
                city=person2_birth_place.split(",")[0].strip() if "," in person2_birth_place else person2_birth_place,
                nation=person2_birth_place.split(",")[1].strip() if "," in person2_birth_place else "US",
                lng=person2_lng,
                lat=person2_lat,
                houses_system_identifier=mapped_house_system,
                tz_str=timezone
            )
            
            # Generate reports
            report1 = Report(person1)
            report2 = Report(person2)
            
            # Process first person's report
            report1_text = report1.get_full_report()
            report1_parts = report1_text.split('\n')
            title1 = report1_parts[0].strip() if report1_parts else f"Kerykeion report for {person1_name}"
            
            # Extract table components from first report
            data_table_start1 = report1_text.find("+-----------+")
            data_table_end1 = report1_text.find("+-----------------+------+")
            planets_table_start1 = data_table_end1
            planets_table_end1 = report1_text.find("+----------------+------+")
            houses_table_start1 = planets_table_end1
            houses_table_end1 = len(report1_text)
            
            data_table1 = report1_text[data_table_start1:data_table_end1].strip()
            planets_table1 = report1_text[planets_table_start1:planets_table_end1].strip()
            houses_table1 = report1_text[houses_table_start1:houses_table_end1].strip()
            
            # Process second person's report
            report2_text = report2.get_full_report()
            report2_parts = report2_text.split('\n')
            title2 = report2_parts[0].strip() if report2_parts else f"Kerykeion report for {person2_name}"
            
            # Extract table components from second report
            data_table_start2 = report2_text.find("+-----------+")
            data_table_end2 = report2_text.find("+-----------------+------+")
            planets_table_start2 = data_table_end2
            planets_table_end2 = report2_text.find("+----------------+------+")
            houses_table_start2 = planets_table_end2
            houses_table_end2 = len(report2_text)
            
            data_table2 = report2_text[data_table_start2:data_table_end2].strip()
            planets_table2 = report2_text[planets_table_start2:planets_table_end2].strip()
            houses_table2 = report2_text[houses_table_start2:houses_table_end2].strip()
            
            # TODO: Generate aspects table when Kerykeion has direct support for synastry aspects
            aspects_table = "Synastry aspects analysis is not yet implemented."
            
            # Create the structured response
            result = {
                "person1": {
                    "title": title1,
                    "data_table": data_table1,
                    "planets_table": planets_table1,
                    "houses_table": houses_table1
                },
                "person2": {
                    "title": title2,
                    "data_table": data_table2,
                    "planets_table": planets_table2,
                    "houses_table": houses_table2
                }
            }
            
            # If using Whole Sign houses, add a note in the logs
            if mapped_house_system == "W":
                logger.info("Using Whole Sign houses system for synastry report")
            
            logger.info("Successfully generated synastry report")
            return result
            
        except Exception as e:
            logger.error(f"Error generating synastry report: {str(e)}")
            raise ReportGenerationError(f"Failed to generate synastry report: {str(e)}")
            
    def _map_house_system(self, house_system: str) -> str:
        """Map house system names to their single-letter codes for Kerykeion.
        
        Args:
            house_system: The human-readable house system name
            
        Returns:
            str: The single-letter house system code
        """
        # Define mapping consistent with ChartVisualizationService
        HOUSE_SYSTEM_MAP = {
            "Placidus": "P",
            "Koch": "K",
            "Whole Sign": "W",
            "Equal House": "A",  # Equal (Ascendant)
            "Equal": "A",       # Alias for Equal House
            "Equal (MC)": "E",
            "Campanus": "C",
            "Regiomontanus": "R",
            "Porphyry": "O",    # Porphyrius
            "Porphyrius": "O",  # Alias for Porphyry
            "Polich Page": "T", # Polich-Page Topocentric
            "Polich-Page Topocentric": "T",
            "Alcabitius": "B",
            "Alcabitus": "B",   # Alias for Alcabitius
            "Morinus": "M",
            "Vehlow Equal": "V",
            "Axial Rotation": "X",
            "Horizon/Azimuth": "H",
            "APC": "Y"
        }
        
        if house_system in HOUSE_SYSTEM_MAP:
            mapped = HOUSE_SYSTEM_MAP[house_system]
            logger.debug(f"Mapped house system '{house_system}' to '{mapped}'")
            return mapped
        
        # If it's already a valid single-letter identifier, return it
        if house_system in "ABCDEFGHIKLMNOPQRSTUVWXY":
            return house_system
        
        # Default to Placidus if not found
        logger.warning(f"Unknown house system '{house_system}', defaulting to Placidus (P)")
        return "P" 