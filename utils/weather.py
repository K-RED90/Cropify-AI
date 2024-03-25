from langchain.pydantic_v1 import BaseModel, root_validator
from langchain.utils.env import get_from_dict_or_env
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from unix_time_converter import unix_utc_to_datetime

load_dotenv()


class GeoData(BaseModel):
    owm: Any
    openweathermap_api_key: Optional[str] = None

    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        openweathermap_api_key = get_from_dict_or_env(
            values, "openweathermap_api_key", "OPENWEATHERMAP_API_KEY"
        )

        try:
            import pyowm

        except ImportError:
            raise ImportError(
                "pyowm is not installed. Please install it with `pip install pyowm`"
            )

        owm = pyowm.OWM(openweathermap_api_key)
        values["owm"] = owm

        return values
    

    def get_location_name(self, lat: float, lon: float, limit: int = 1):
        gem = self.owm.geocoding_manager()
        locations = gem.reverse_geocode(lat, lon, limit = limit)
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
   
    def get_weather(self, lat:float, lon: float) -> str:
        """Get the current weather information for a specified lat and lon."""
        mgr = self.owm.weather_manager()
        observation = mgr.weather_at_coords(lat, lon)
        w = observation.weather
        climate_data = self._format_weather_info(w)

        return climate_data
    

# gd = GeoData()

# print(gd.get_weather(6.6642, -1.8169))