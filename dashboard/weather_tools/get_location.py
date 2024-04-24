from typing import Any, Type
from .base import BaseOpenWeatherMap
from langchain_core.pydantic_v1 import BaseModel, Field
from asyncer import asyncify


class LocationSchema(BaseModel):
    lat: float = Field(description="Latitude of the location")
    lon: float = Field(description="Longitude of the location")



class GetCurrentLocation(BaseOpenWeatherMap):
    name = "get_current_location"
    description = "Get the current location of the users corrdinates"
    args_schema: Type[BaseModel] = LocationSchema

    def _run(self, lat, lon):
        gem = self.owm.geocoding_manager()
        location = gem.reverse_geocode(lat, lon, limit=1)
        return location
    
    def _arun(self, *args: Any, **kwargs: Any):
        return asyncify(self._run, cancellable=True)(*args, **kwargs)
        