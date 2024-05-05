from langchain_core.pydantic_v1 import BaseModel, root_validator
from langchain_core.utils import get_from_dict_or_env
from typing import Any, Optional
from langchain_core.tools import BaseTool


class BaseOpenWeatherMap(BaseTool):
    owm: Optional[Any] = None
    api_key: Any = None

    @root_validator
    def validate_api(cls, values: dict):
        if values.get("owm") is None:
            try:
                import pyowm
            except ImportError:
                raise ImportError(
                    "Please, install openweathermap api. `pip install pyowm`"
                )
        api_key = get_from_dict_or_env(
            values, "openweathermap_api_key", "OPENWEATHERMAP_API_KEY"
        )
        owm = pyowm.OWM(api_key=api_key)
        values["owm"] = owm
        return values
