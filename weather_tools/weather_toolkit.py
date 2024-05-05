from typing import List
from langchain_community.agent_toolkits.base import BaseToolkit
from langchain_community.tools import BaseTool
from .get_location import GetCurrentLocation
from .get_weather_data import GetWeatherDataByCordinates, GetWeatherDataByCityName
from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit


class WeatherToolkit(BaseToolkit):

    def get_tools(self) -> List[BaseTool]:
        return [
            GetWeatherDataByCordinates(),
            GetWeatherDataByCityName(),
            GetCurrentLocation(),
        ]
