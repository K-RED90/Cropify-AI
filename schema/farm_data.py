from pydantic import BaseModel,  EmailStr
from typing import Literal, List, Optional, Dict, Any
class FarmData(BaseModel):
    crop:str
    pests:List[str]
    diseases:List[str]
    soil_type: str
    soil_ph:str
    pct_soil_moisture:str
    soil_fertility:str
    user:str
    lon:str
    lat:str 
    



