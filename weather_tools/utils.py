from datetime import datetime, timezone
from typing import Any


def unix_utc_to_datetime(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)


def format_weather_info(w: Any) -> str:
    status = w.status
    wind = w.wind()
    humidity = w.humidity
    temperature = w.temperature("celsius")
    heat_index = w.heat_index
    clouds = w.clouds
    pressure = w.pressure
    precipitation_probability = w.precipitation_probability

    return {
        "status": status,
        "wind": f"{wind['speed']} m/s, direction: {wind['deg']}°",
        "humidity": f"{humidity}%",
        "temperature": f"{temperature['temp']}°C",
        "heat_index": heat_index,
        "clouds": f"{clouds}%",
        "pressure": f"{pressure['press']} hPa",
        "precipitation_probability": (
            f"{precipitation_probability}%" if precipitation_probability else None
        ),
    }
