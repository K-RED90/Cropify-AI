from typing import Any, Annotated, Sequence
from dotenv import load_dotenv
from .unix_time_converter import unix_utc_to_datetime
from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper

load_dotenv()


class WeatherAPI(OpenWeatherMapAPIWrapper):
    
    @classmethod
    def add_method(cls, func):
        setattr(cls, func.__name__, func)
        return func

    def get_location_name(self, cordinates: Annotated[Sequence[float], "Cordinates of the location (lat, lon)"], limit: int = 1):
        gem = self.owm.geocoding_manager()
        locations = gem.reverse_geocode(*cordinates, limit = limit)
        return locations
    

    def _format_weather_info(self, w: Any) -> str:
        detailed_status = w.detailed_status
        reference_time = unix_utc_to_datetime(w.reference_time())
        sunset_time = unix_utc_to_datetime(w.sunset_time())
        sunrise_time = unix_utc_to_datetime(w.sunrise_time())
        status = w.status
        wind = w.wind()
        humidity = w.humidity
        temperature = w.temperature("celsius")
        rain = w.rain
        heat_index = w.heat_index
        clouds = w.clouds
        pressure = w.pressure
        precipitation_probability = w.precipitation_probability

        return {
            "detail_status": detailed_status,
            "reference_time": reference_time,
            "sunset_time": sunset_time,
            "sunrise_time": sunrise_time,
            "wind": f"{wind['speed']} m/s, direction: {wind['deg']}°",
            "humidity": f"{humidity}%",
            "temperature": {
                "current": f"{temperature['temp']}°C",
                "high": f"{temperature['temp_max']}°C",
                "low": f"{temperature['temp_min']}°C",
                "feels_like": f"{temperature['feels_like']}°C",
            },
            "status": status,
            "rain": rain,
            "heat_index": heat_index,
            "clouds": f"{clouds}%",
            "pressure": f"{pressure['press']} hPa",
            "precipitation_probability": f"{precipitation_probability}%" if precipitation_probability else None,

        }
   
    def run(self, cordinates: Annotated[Sequence[float], "Cordinates of the location (lat, lon)"]) -> str:
        """Get the current weather information for a specified lat and lon."""
        mgr = self.owm.weather_manager()
        observation = mgr.weather_at_coords(*cordinates)
        w = observation.weather
        climate_data = self._format_weather_info(w)

        return climate_data
    

# gd = WeatherAPI()

# print(gd(6.6642, -1.8169))