from .base import BaseOpenWeatherMap
from langchain_core.pydantic_v1 import BaseModel
from typing import Any, Type
from asyncer import asyncify
from .get_location import LocationSchema
from .utils import format_weather_info


class GetWeatherDataByCordinates(BaseOpenWeatherMap):
    name = "get_weather_data_by_cordinates"
    description = "Get the weather data by the cordinates of the location"
    args_schema: Type[BaseModel] = LocationSchema

    def _run(self, lat, lon):
        mgr = self.owm.weather_manager()
        observation = mgr.weather_at_coords(lat, lon)
        w = observation.weather
        climate_data = format_weather_info(w)
        return climate_data

    async def _arun(self, *args: Any, **kwargs: Any):
        return await asyncify(self._run, cancellable=True)(*args, **kwargs)


class GetWeatherDataByCityName(BaseOpenWeatherMap):
    name = "get_weather_data_by_city_name"
    description = "Get the weather data by the city name"

    def _run(self, city_name):
        mgr = self.owm.weather_manager()
        observation = mgr.weather_at_place(city_name)
        w = observation.weather
        climate_data = format_weather_info(w)
        return climate_data

    async def _arun(self, *args: Any, **kwargs: Any):
        return await asyncify(self._run, cancellable=True)(*args, **kwargs)
