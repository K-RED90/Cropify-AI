from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union, Dict


class SoilSchema(BaseModel):
    soil_type: Literal["Clay", "Sandy", "Loamy", "Chalky", "Silt"]
    # soil_depth: Literal["Very shallow (less than 15 cm)", "Shallow (15-30 cm)", "Moderately deep (30-60 cm)", "Deep (more than 60 cm)"] = Field(..., title="Soil Depth", description="the thickness of the soil layer that extends from the surface to the unweathered bedrock or saprolite beneath.",)
    soil_ph: Literal["Strong acidic (3.5–4.4)", "Acidic (4.5-6.5)", "Neutral (6.6–7.3)", "Alkaline (7.4-9)", "Strongly alkaline: > 9.0"] = Field(..., title="Soil pH", description="a measure of the acidity or alkalinity of soil and is measured in pH units.",)
    pct_soil_moisture: float = Field(..., title="Soil Moisture", description="the water that is held in the spaces between soil particles.", ge=0, le=100,)
    # nutrients_proportion: Dict[str, float] = Field(..., title="Nutrients Proportion", description="Proportion of nutrients in the soil")
    soil_fertility : Literal["Low", "Medium", "High"] = Field(..., title="Soil Fertility", description="the ability of soil to provide essential nutrients to plants.",)
    # irrigation: Literal["Rainfed", "Irrigated", "Partially irrigated"] = Field(..., title="Irrigation", description="the artificial application of water to the soil to assist in the growth of crops.",)