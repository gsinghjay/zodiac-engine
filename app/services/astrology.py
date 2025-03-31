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
    ) -> NatalChartResponse:
        """Calculate natal chart for given parameters."""
        try:
            logger.info(f"Calculating natal chart for {name} born on {birth_date}")
            logger.debug(f"Location data: city={city}, nation={nation}, lng={lng}, lat={lat}, tz={tz_str}")

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
            )

            logger.debug("Created AstrologicalSubject successfully")

            # Calculate aspects
            aspects = NatalAspects(subject)
            logger.debug("Calculated aspects successfully")

            # Get planet positions
            planets = []
            for planet_attr in ['sun', 'moon', 'mercury', 'venus', 'mars', 
                            'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']:
                planet = getattr(subject, planet_attr)
                planets.append(PlanetPosition(
                    name=planet_attr.capitalize(),
                    sign=planet.sign,
                    position=planet.position,
                    house=_convert_house_number(planet.house),
                    retrograde=planet.retrograde
                ))
            logger.debug(f"Processed {len(planets)} planets successfully")

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

            response = NatalChartResponse(
                name=name,
                birth_date=birth_date,
                planets=planets,
                houses=houses,
                aspects=[AspectInfo(
                    p1_name=aspect.p1_name,
                    p2_name=aspect.p2_name,
                    aspect=aspect.aspect,
                    orbit=aspect.orbit
                ) for aspect in aspects.all_aspects]
            )
            logger.info("Successfully created natal chart response")
            return response
        except Exception as e:
            logger.error(f"Error calculating natal chart: {str(e)}", exc_info=True)
            raise 