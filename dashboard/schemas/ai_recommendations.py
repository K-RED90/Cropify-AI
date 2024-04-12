from typing import List, Dict, Any, Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


class PestAndDiseasePrevention(BaseModel):
    """Extract recommendations for pest and disease prevention based on farm data."""
    recommendations: List[str] = Field(description="List of recommendations for pest and disease prevention based on farm data")

class PestAndDiseaseTreatment(BaseModel):
    """Extract recommendations for pest and disease treatment based on farm data."""
    organic: str = Field(description="organic treatments for pest and disease")
    chemical: str = Field(description="chemical treatments for pest and disease")

class PestAndDiseaseCauses(BaseModel):
    """Extract causes of pest and disease based on farm data."""
    causes_of_pests: List[str] = Field(description="Causes of pests")
    causes_of_diseases: List[str] = Field(description="Causes of diseases")

class PestAndDiseaseControl(BaseModel):
    """Extract recommendations for pest and disease control based on farm data."""
    causes: PestAndDiseaseCauses
    prevention: PestAndDiseasePrevention
    treatment: PestAndDiseaseTreatment


class EarlyGrowthRecommendations(BaseModel):
    """Weed control recommendations for seedling/early growth stage"""
    key_weeds: List[str] = Field(description="Key weed species to target")
    pre_emergent_herbicides: str = Field(description="Pre-emergent herbicides recommendations")
    cultural_controls: str = Field(description="Cultural/mechanical control measures")
    application_details: str = Field(description="Application rates, timing, and precautions")

class MidSeasonRecommendations(BaseModel):
    """Weed control recommendations for mid-season growth stage"""
    in_crop_strategies: str = Field(description="Targeted in-crop weed control strategies")
    selective_herbicides: str = Field(description="Selective post-emergent herbicides recommendations")
    weather_considerations: str = Field(description="Weather-related factors to consider")

class LateSeasonRecommendations(BaseModel):
    """Weed control recommendations for late-season/harvest stage"""
    late_emerging_weeds: str = Field(description="Methods for late-emerging/hard-to-control weeds")
    desiccants_harvest_aids: str = Field(description="Desiccants, harvest aids recommendations")
    re_cropping_concerns: str = Field(description="Re-cropping intervals and carryover concerns")

class WeedControlRecommendations(BaseModel):
    """Detailed weed control recommendations by crop growth stage"""
    early_growth: EarlyGrowthRecommendations
    mid_season: MidSeasonRecommendations
    late_season: LateSeasonRecommendations

    
class SoilHealthRecommendations(BaseModel):
    """
    Recommendations for improving soil health.
    """
    soil_amendments: List[str]
    cover_cropping_strategies: List[str]
    tillage_practices: List[str]
    organic_matter_management: str

class CropNutrientManagement(BaseModel):
    """
    Recommendations for crop nutrient management.
    """
    macronutrient_requirements: str
    micronutrient_requirements: str
    fertilization_program: str
    organic_vs_synthetic_considerations: str

class IntegratedCropManagement(BaseModel):
    """
    Recommendations for integrated crop management.
    """
    irrigation_scheduling: str
    irrigation_techniques: str
    pest_and_disease_control: str
    harvest_and_post_harvest: str

class SoilHealthAndCropManagementPlan(BaseModel):
    """
    Extracted the comprehensive soil health and crop management plan.
    """
    soil_health_recommendations: SoilHealthRecommendations
    crop_nutrient_management: CropNutrientManagement
    integrated_crop_management: IntegratedCropManagement