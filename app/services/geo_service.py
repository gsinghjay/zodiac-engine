"""Geo service for location-based functionality."""

import logging
import os
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from requests import Request
from requests_cache import CachedSession
from datetime import timedelta

from app.core.config import settings


# Define response models
class GeoLocation(BaseModel):
    """Location data with coordinates and timezone."""
    name: str
    country_code: str
    latitude: float
    longitude: float
    timezone: str


class GeoService:
    """Service for handling geolocation requests."""
    
    def __init__(self):
        """Initialize the geo service with cache session."""
        cache_dir = os.path.join(os.getcwd(), "cache")
        os.makedirs(cache_dir, exist_ok=True)
        
        self.session = CachedSession(
            cache_name="cache/zodiac_geonames_cache",
            backend="sqlite",
            expire_after=timedelta(days=30),
        )
        
        # Check if username is properly set
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Settings GEONAMES_USERNAME value: '{settings.GEONAMES_USERNAME}'")
        
        # Only use non-empty username values
        if settings.GEONAMES_USERNAME and settings.GEONAMES_USERNAME.strip():
            self.username = settings.GEONAMES_USERNAME.strip()
            self.logger.info(f"Using GeoNames username: {self.username}")
        else:
            self.username = "demo"
            self.logger.warning("No GEONAMES_USERNAME set in .env or it's empty. Using demo mode with limited functionality.")
        
        self.base_url = "http://api.geonames.org/searchJSON"
        self.timezone_url = "http://api.geonames.org/timezoneJSON"
    
    async def search_cities(self, query: str, max_rows: int = 10) -> List[GeoLocation]:
        """
        Search for cities matching the query.
        
        Args:
            query: Search string for city name
            max_rows: Maximum number of results to return (default: 10)
            
        Returns:
            List of locations with coordinates and timezone
        """
        if self.username == "demo":
            self.logger.warning("Using demo mode with limited functionality. The API may refuse service if demo limit is exceeded.")
        
        params = {
            "q": query,
            "maxRows": max_rows,
            "username": self.username,
            "style": "MEDIUM",
            "featureClass": "P",  # Populated places
        }
        
        prepared_request = Request("GET", self.base_url, params=params).prepare()
        self.logger.debug(f"Requesting city data from GeoNames: {prepared_request.url}")
        
        try:
            response = self.session.send(prepared_request)
            response_json = response.json()
            
            if "status" in response_json:
                # Error response
                error_msg = response_json.get("status", {}).get("message", "Unknown GeoNames error")
                self.logger.error(f"GeoNames API error: {error_msg}")
                return []
            
            results = []
            for place in response_json.get("geonames", []):
                # For each place, get the timezone
                timezone = await self._get_timezone(place.get("lat"), place.get("lng"))
                
                results.append(GeoLocation(
                    name=place.get("name", ""),
                    country_code=place.get("countryCode", ""),
                    latitude=float(place.get("lat", 0)),
                    longitude=float(place.get("lng", 0)),
                    timezone=timezone
                ))
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error fetching data from GeoNames: {e}")
            return []
    
    async def _get_timezone(self, lat: str, lng: str) -> str:
        """
        Get timezone for given coordinates.
        
        Args:
            lat: Latitude
            lng: Longitude
            
        Returns:
            Timezone string (e.g., 'America/New_York')
        """
        params = {
            "lat": lat,
            "lng": lng,
            "username": self.username
        }
        
        prepared_request = Request("GET", self.timezone_url, params=params).prepare()
        self.logger.debug(f"Requesting timezone data from GeoNames: {prepared_request.url}")
        
        try:
            response = self.session.send(prepared_request)
            response_json = response.json()
            
            if "status" in response_json:
                # Error response
                error_msg = response_json.get("status", {}).get("message", "Unknown GeoNames error")
                self.logger.error(f"GeoNames API error when fetching timezone: {error_msg}")
                return ""
            
            return response_json.get("timezoneId", "")
            
        except Exception as e:
            self.logger.error(f"Error fetching timezone from GeoNames: {e}")
            return "" 