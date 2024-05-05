from weather_tools import (
    GetCurrentLocation,
    GetWeatherDataByCityName,
    GetWeatherDataByCordinates,
)
from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.get("/current-location/{latitude}/{longitude}", tags=["weather"])
async def get_current_location(latitude: float, longitude: float):
    """
    Get the current location based on the provided latitude and longitude.
    """
    try:
        get_location = GetCurrentLocation()
        location = get_location.invoke({"lat": latitude, "lon": longitude})
        return {"location": location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/weather-by-city/{city_name}", tags=["weather"])
async def get_weather_by_city(city_name: str):
    """
    Get the weather data for a given city.
    """
    try:
        by_city = GetWeatherDataByCityName()
        weather_data = by_city.invoke({"city_name": city_name})
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/weather-by-coordinates/{latitude}/{longitude}", tags=["weather"])
async def get_weather_by_coordinates(latitude: float, longitude: float):
    """
    Get the weather data for a given set of coordinates.
    """
    try:
        by_coordinates = GetWeatherDataByCordinates()
        weather_data = by_coordinates.invoke({"lat": latitude, "lon": longitude})
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))