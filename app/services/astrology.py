"""Service for astrological calculations using Kerykeion."""
import logging
from datetime import datetime
from typing import Dict, List, Union

from kerykeion import AstrologicalSubject, NatalAspects

from app.schemas.natal_chart import NatalChartResponse, PlanetPosition, AspectInfo

logger = logging.getLogger(__name__)

def _convert_house_number(house: Union[str, int]) -> Union[str, int]:
    """Convert house number from string to int if possible."""
    if isinstance(house, int):
        return house
    try:
        # Try to extract number from string like "First_House"
        house_map = {
            "First": 1, "Second": 2, "Third": 3, "Fourth": 4,
            "Fifth": 5, "Sixth": 6, "Seventh": 7, "Eighth": 8,
            "Ninth": 9, "Tenth": 10, "Eleventh": 11, "Twelfth": 12
        }
        for name, num in house_map.items():
            if name in house:
                return num
        # If we can't map it, return the original string
        return house
    except (ValueError, AttributeError):
        return house

class AstrologyService:
    """Service for astrological calculations using Kerykeion."""

    @staticmethod
    def calculate_natal_chart(
        name: str,
        birth_date: datetime,
        city: str | None = None,
        nation: str | None = None,
        lng: float | None = None,
        lat: float | None = None,
        tz_str: str | None = None,
        houses_system: str = "P",  # Default to Placidus
    ) -> NatalChartResponse:
        """Calculate natal chart for given parameters."""
        try:
            logger.info(f"Calculating natal chart for {name} born on {birth_date}")
            logger.debug(f"Location data: city={city}, nation={nation}, lng={lng}, lat={lat}, tz={tz_str}")
            logger.debug(f"House system: {houses_system}")

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
                houses_system_identifier=houses_system,
            )

            logger.debug("Created AstrologicalSubject successfully")

            # Calculate aspects
            aspects = NatalAspects(subject)
            logger.debug("Calculated aspects successfully")

            # Get planet positions - including additional celestial points
            planets = []
            standard_planets = [
                'sun', 'moon', 'mercury', 'venus', 'mars', 
                'jupiter', 'saturn', 'uranus', 'neptune', 'pluto'
            ]
            
            # Additional celestial points from Data Completeness requirements
            additional_points = [
                'mean_node', 'true_node', 'mean_south_node', 'true_south_node',
                'mean_lilith', 'chiron'
            ]
            
            # Process standard planets
            for planet_attr in standard_planets:
                planet = getattr(subject, planet_attr)
                planets.append(PlanetPosition(
                    name=planet_attr.capitalize(),
                    sign=planet.sign,
                    position=planet.position,
                    house=_convert_house_number(planet.house),
                    retrograde=planet.retrograde
                ))
            
            # Process additional celestial points
            for point_attr in additional_points:
                point = getattr(subject, point_attr, None)
                if point is not None:  # Some points may be None if disabled
                    # Convert names for better readability
                    display_name = point_attr.replace('_', ' ').title()
                    planets.append(PlanetPosition(
                        name=display_name,
                        sign=point.sign,
                        position=point.position,
                        house=_convert_house_number(point.house),
                        retrograde=getattr(point, 'retrograde', False)  # Some points don't have retrograde status
                    ))
            
            logger.debug(f"Processed {len(planets)} planets and points successfully")

            # Get house cusps using individual house attributes
            houses = {}
            house_attrs = [
                'first_house', 'second_house', 'third_house', 'fourth_house',
                'fifth_house', 'sixth_house', 'seventh_house', 'eighth_house',
                'ninth_house', 'tenth_house', 'eleventh_house', 'twelfth_house'
            ]
            for i, attr in enumerate(house_attrs, 1):
                house = getattr(subject, attr)
                houses[i] = house.position
            logger.debug("Processed house cusps successfully")

            # Include complete aspect data with orbs
            aspect_info = []
            for aspect in aspects.all_aspects:
                aspect_info.append(AspectInfo(
                    p1_name=aspect.p1_name,
                    p2_name=aspect.p2_name,
                    aspect=aspect.aspect,
                    orbit=aspect.orbit,
                ))
            
            # Get house system information
            house_system_name = subject.houses_system_name
            house_system_id = subject.houses_system_identifier
            
            response = NatalChartResponse(
                name=name,
                birth_date=birth_date,
                planets=planets,
                houses=houses,
                aspects=aspect_info,
                house_system={
                    "name": house_system_name,
                    "identifier": house_system_id
                }
            )
            logger.info("Successfully created natal chart response")
            return response
        except Exception as e:
            logger.error(f"Error calculating natal chart: {str(e)}", exc_info=True)
            raise 