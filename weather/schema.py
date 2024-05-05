from typing import Optional, Union
from pydantic import BaseModel, validator

class Weather(BaseModel):
    status: Optional[str] = None
    wind: str
    humidity: str
    temperature: str
    heat_index: Optional[Union[float, str, None]] = None
    clouds: str
    pressure: str
    precipitation_probability: Optional[Union[float, str, None]] = None

    @validator("heat_index", "precipitation_probability", pre=True)
    def parse_optional_float(cls, value):
        if value is None:
            return value
        try:
            return float(value)
        except ValueError:
            return value
