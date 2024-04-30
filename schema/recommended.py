from pydantic import BaseModel,  EmailStr
from typing import Literal, List, Optional, Dict, Any
class Recommended(BaseModel):
    pestRecommended:str
    soilRecommended:str
    user:str
    crop:str
  
    
    



