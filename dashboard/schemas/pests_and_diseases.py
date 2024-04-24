from pydantic import BaseModel, Field
from typing import Literal, List, Optional, Dict, Any
import json


class PestsAndDiseasesSchema(BaseModel):
    pests: List[str] | str | None = Field(None, title="Pests", description="pests affecting the crop")
    diseases : List[str] | str | None = Field(None, title="Diseases", description="diseases affecting the crop")
    # damage: str = Field(..., title="Damage", description="Damage caused by the pest")

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str):
        return cls.from_dict(json.loads(json_str))
    
    class Config:
        json_schema_extra = {
            "example": {
                "pests": ["Aphids", "Thrips", "Whiteflies"],
                "diseases": ["Powdery Mildew", "Downy Mildew", "Fusarium Wilt"],
                "damage": "Yellowing of leaves, stunted growth, and curling of leaves"
            }
        }

