from typing import Optional, Union
from pydantic import BaseModel, validator


class Rain(BaseModel):
    pass


class Weather(BaseModel):
    detail_status: str
    reference_time: str
    sunset_time: str
    sunrise_time: str
    wind: str
    humidity: str
    temperature: str
    status: str
    rain: Rain
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
