from .base import BaseOpenWeatherMap
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Any, Type
from asyncer import asyncify
from .get_location import LocationSchema
from .utils import format_weather_info, unix_utc_to_datetime
import json
from datetime import timedelta
import math


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


class WeatherInputSchema(BaseModel):
    city_name: str = Field(
        description="City name for which you want to get the weather data"
    )


class GetWeatherDataByCityName(BaseOpenWeatherMap):
    name = "get_weather_data_by_city_name"
    description = "Useful to get the current weather data given a city_name"
    args_schema: Type[BaseModel] = WeatherInputSchema

    def _run(self, city_name):
        mgr = self.owm.weather_manager()
        try:
            observation = mgr.weather_at_place(city_name)
            w = observation.weather
            climate_data = format_weather_info(w)
            return climate_data
        except Exception as e:
            return f"Cannot find the weather data for the city {city_name}. Check the city name."

    async def _arun(self, *args: Any, **kwargs: Any):
        return await asyncify(self._run, cancellable=True)(*args, **kwargs)


class ForecastInputSchema(BaseModel):
    city_name: str = Field(
        description="City name for which you want to get the weather forecast data. Eg. Accra,GH"
    )
    limit: int = Field(
        5, description="the maximum number of *Weather* items to be retrieved. The weather is forecasted every 3 hours so for example the limit for tomorrow's weather is 24/3"
    )


class GetWeatherForecastByCityName(BaseOpenWeatherMap):
    name = "get_weather_forecast"
    description = "Useful to get weather forecast data given a city_name for every 3h interval"
    args_schema: Type[BaseModel] = ForecastInputSchema

    def _run(self, city_name, limit=5):
        mgr = self.owm.weather_manager()
        try:
            forecast = mgr.forecast_at_place(city_name, "3h", limit=limit).forecast
            reception_time = unix_utc_to_datetime(forecast.reception_time())
            forecast_data = ""
            i = 3
            for weather in forecast:
                forecast_data += f"{reception_time + timedelta(hours=i)}: {json.dumps(format_weather_info(weather))}\n"
                i += 3
            return forecast_data
        except Exception as e:
            return f"Cannot find the weather forecast data for the city {city_name}. Check the city name."

    async def _arun(self, *args: Any, **kwargs: Any):
        return await asyncify(self._run, cancellable=True)(*args, **kwargs)
