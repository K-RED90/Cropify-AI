from pydantic import BaseModel

class Weather(BaseModel):
    lat:str
    lon:str