from pydantic import BaseModel, Field
from typing import Literal, Dict
import json


class FertilizerSchema(BaseModel):
    fertilizer_type: Literal["Organic", "Inorganic", "Biofertilizer", "Fertilizer Mix", "Fertilizer Blend"] = Field(..., title="Fertilizer Type", description="Type of fertilizer")
    frequency_of_application: Literal["Once", "Twice", "Thrice", "Four times", "More than four times"] = Field(..., title="Frequency of Application", description="Number of times the fertilizer is applied in a year")
    nutrient_proportion: Dict[str, float] = Field(..., title="Nutrient Proportion", description="Proportion of nutrients in the fertilizer")
    nutrient_form: Literal["Solid", "Liquid", "Gas"] = Field(..., title="Nutrient Form", description="the physical form of the nutrient in the fertilizer.",)
    nutrient_availability: Literal["Quick-release", "Slow-release"] = Field(..., title="Nutrient Availability", description="the rate at which the nutrient is available to the plant.",)
    nutrient_role: Literal["Growth", "Development", "Reproduction"] = Field(..., title="Nutrient Role", description="the function of the nutrient in plant growth and development.")
    

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str):
        return cls.from_dict(json.loads(json_str))
    
    class Config:
        schema_extra = {
            "example": {
                "fertilizer_type": "Organic",
                "frequency_of_application": "Twice",
                "nutrient_proportion": {"Nitrogen": 10, "Phosphorus": 5, "Potassium": 5},
                "nutrient_form": "Solid",
                "nutrient_availability": "Quick-release",
                "nutrient_role": "Growth",
            }
        }
    
