from typing import List, Dict, Any
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class RecommendationsSchema(BaseModel):

    crop_management: List[str] = Field(default=[], title="Crop Management", description="4 tailored crop management practices")
    fertilizers: Dict[str, Any] = Field(default={}, title="Fertilizers", description="Specific fertilizer type, nutrient composition, and application rates")
    application_method: str = Field(default="", title="Application Method", description="Specific method of fertilizer application")
    application_timing: Dict[str, Any] = Field(default={}, title="Application Timing", description="Timing of fertilizer application with crop stage and rate")
    nutrient_role: Dict[str, str] = Field(default={}, title="Nutrient Role", description="Role of each nutrient in plant growth and development")
    pest_control_measures: List[str] = Field(default=[{}], title="Pest Control Measures", description="Specific pest control measures including pesticides, application rates, and timing")
    disease_prevention: List[str] = Field(default=[], title="disease prevention", description="Specific disease prevention measures")
    fungicides: Dict[str, Any] = Field(default={}, title="fungicide", description="fungicide, application rates, and timing")
    weeds_control_measure: List[str] = Field(default=[], title="Weeds Control Measure", description="Specific weed control measures, including weedicide with application rate and timing")
    # herbicides: List[str] = Field(..., title="Herbicide", description="Specific herbicides with application rates and timing")
    soil_health: List[str] = Field(default=[], title="Soil Health", description="Specific soil health practices")
    weather_adaptation: List[str] = Field(default=[], title="Weather Adaptation", description="Specific weather adaptation practices")
    

    @classmethod
    def get_format_instructions(cls):
        output_parser = PydanticOutputParser(pydantic_object=cls)
        format_instructions = output_parser.get_format_instructions()
        return output_parser, format_instructions
    
