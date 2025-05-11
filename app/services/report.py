"""Service for generating astrological reports using Kerykeion's Report class."""
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from kerykeion import AstrologicalSubject, Report
from app.services.chart_visualization import map_house_system

logger = logging.getLogger(__name__)

class ReportService:
    """Service for generating astrological reports from chart data."""

    def generate_natal_report(
        self,
        name: str,
        birth_date: datetime,
        city: str | None = None,
        nation: str | None = None,
        lng: float | None = None,
        lat: float | None = None,
        tz_str: str | None = None,
        houses_system: str = "P",  # Default to Placidus
    ) -> Dict[str, str]:
        """
        Generate a report for a natal chart using Kerykeion's Report class.
        
        Args:
            name: Name of the person
            birth_date: Date and time of birth
            city: Optional city of birth
            nation: Optional country of birth
            lng: Optional longitude of birth place
            lat: Optional latitude of birth place
            tz_str: Optional timezone string
            houses_system: House system identifier (can be human-readable name or single-letter code)
            
        Returns:
            Dictionary containing various report sections as strings
        """
        try:
            logger.info(f"Generating natal report for {name} born on {birth_date}")
            
            # Map house system to Kerykeion-compatible format
            mapped_houses_system = map_house_system(houses_system)
            logger.debug(f"Mapped house system from '{houses_system}' to '{mapped_houses_system}'")
            
            # Set default timezone if None
            if tz_str is None:
                logger.warning("No timezone provided for natal report, defaulting to UTC")
                tz_str = "UTC"
            
            # Create AstrologicalSubject
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
                houses_system_identifier=mapped_houses_system,
            )
            
            logger.debug("Created AstrologicalSubject successfully")
            
            # Generate report using Kerykeion's Report class
            report = Report(subject)
            
            # Extract report components
            report_data = {
                "title": report.report_title,
                "data_table": report.data_table,
                "planets_table": report.planets_table,
                "houses_table": report.houses_table,
                "full_report": report.get_full_report()
            }
            
            logger.info("Successfully generated natal report")
            return report_data
            
        except Exception as e:
            logger.error(f"Error generating natal report: {str(e)}", exc_info=True)
            raise

    def generate_synastry_report(
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
        houses_system: str = "P",  # Default to Placidus
    ) -> Dict[str, Any]:
        """
        Generate reports for two charts in a synastry comparison.
        
        Args:
            Parameters for both individuals' birth details
            houses_system: House system identifier (can be human-readable name or single-letter code)
            
        Returns:
            Dictionary containing report data for both charts
        """
        try:
            logger.info(f"Generating synastry report for {name1} and {name2}")
            
            # Map house system to Kerykeion-compatible format
            mapped_houses_system = map_house_system(houses_system)
            logger.debug(f"Mapped house system from '{houses_system}' to '{mapped_houses_system}'")
            
            # Set default timezones if None
            if tz_str1 is None:
                logger.warning(f"No timezone provided for {name1}, defaulting to UTC")
                tz_str1 = "UTC"
                
            if tz_str2 is None:
                logger.warning(f"No timezone provided for {name2}, defaulting to UTC")
                tz_str2 = "UTC"
            
            # Create AstrologicalSubject for first person
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
                houses_system_identifier=mapped_houses_system,
            )
            
            # Create AstrologicalSubject for second person
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
                houses_system_identifier=mapped_houses_system,
            )
            
            logger.debug("Created AstrologicalSubject instances successfully")
            
            # Generate reports for both subjects
            report1 = Report(subject1)
            report2 = Report(subject2)
            
            # Combine report data
            synastry_report = {
                "person1": {
                    "title": report1.report_title,
                    "data_table": report1.data_table,
                    "planets_table": report1.planets_table,
                    "houses_table": report1.houses_table,
                },
                "person2": {
                    "title": report2.report_title,
                    "data_table": report2.data_table,
                    "planets_table": report2.planets_table,
                    "houses_table": report2.houses_table,
                }
            }
            
            logger.info("Successfully generated synastry report")
            return synastry_report
            
        except Exception as e:
            logger.error(f"Error generating synastry report: {str(e)}", exc_info=True)
            raise 