from datetime import datetime, timezone
from typing import Any

def unix_utc_to_datetime(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)


def format_weather_info(w: Any) -> str:
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
            "temperature": f"{temperature['temp']}°C",
            "status": status,
            "rain": rain,
            "heat_index": heat_index,
            "clouds": f"{clouds}%",
            "pressure": f"{pressure['press']} hPa",
            "precipitation_probability": (
                f"{precipitation_probability}%" if precipitation_probability else None
            ),
        }


