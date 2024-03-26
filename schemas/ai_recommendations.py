from typing import Union, List, Dict, Any
from langchain_core.pydantic_v1 import BaseModel, Field

class FertilizerUse(BaseModel):
    """Use this data model to provide specific fertilizer use recommendations"""
    fertilizers: List[Dict[str, Any]] = Field(..., title="Fertilizers", description="Specific fertilizers with type, nutrient composition, and application rates")
    application_method: str = Field(..., title="Application Method", description="Specific method of fertilizer application")
    application_timing: List[Dict[str, Any]] = Field(..., title="Application Timing", description="Timing of fertilizer application with crop stage and rate")
    nutrient_role: Dict[str, str] = Field(..., title="Nutrient Role", description="Role of each nutrient in plant growth and development")

class PestControl(BaseModel):
    """Use this data model to provide specific pest control measures"""
    scouting: Dict[str, Any] = Field(..., title="Scouting", description="Specific scouting methods and frequency for pest monitoring")
    resistant_varieties: List[str] = Field(..., title="Resistant Varieties", description="Specific pest-resistant crop varieties to plant")
    biological_control: List[Dict[str, Any]] = Field(..., title="biological", description="Specific biological control methods, organisms, and application rates/timing")
    chemical_control: List[Dict[str, Any]] = Field(..., title="chemical control", description="Specific organic insecticides, application rates, and timing")

class DiseaseControl(BaseModel):
    """Use this data model to provide specific disease control measures"""
    prevention: List[Dict[str, Any]] = Field(..., title="disease_prevention", description="Specific disease prevention measures with details")
    fungicides: List[Dict[str, Any]] = Field(..., title="fungicides", description="Specific fungicides, application rates, and timing")

class WeedSuppression(BaseModel):
    weeds_control_measure: List[Dict[str, Any]] = Field(..., title="Weeds Control Measure", description="Specific weed control measures with details")
    herbicides: List[str] = Field(..., title="Herbicides", description="Specific herbicides with application rates and timing")

class GeneralRecommendations(BaseModel):
    """Use this data model to provide tailored recommendations for crop management, soil health, weather adaptation, and sustainable methods"""
    crop_management: List[str] = Field(..., title="Crop Management", description="At least 3 specific crop management practices")
    # fertilizer_use: FertilizerUse
    # pest_control: PestControl
    # disease_control: DiseaseControl
    # weed_suppression: WeedSuppression
    soil_health: List[str] = Field(..., title="Soil Health", description="At least 3 Specific soil health practices")
    weather_adaptation: List[str] = Field(..., title="Weather Adaptation", description="At least 3 Specific weather adaptation practices")
    sustainable_methods: List[str] = Field(..., title="Sustainable Methods", description="At least 3 Specific sustainable farming practices")
