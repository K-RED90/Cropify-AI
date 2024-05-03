from dashboard.crop_dashboard import CropDashboard
from dashboard.prompt_templates import (
    FERTILIZER_SYSTEM_PROMPT,
    PEST_AND_DISEASE_PROMPT,
    WEEDS_CONTROL_PROMPT,
    SOIL_HEALTH_AND_CROP_MANAGEMENT_PROMPT,
)
from .schema import (
    PestAndDiseaseControl,
    WeedControlRecommendations,
    SoilHealthAndCropManagementPlan,
    PestDiseaseControlRecommendations
)
from .schema import FarmDataSchema
from weather.schema import Weather
from fastapi import APIRouter, HTTPException
from models import load_llm


router = APIRouter()

# Initialize the LLM and CropDashboard
llm = load_llm(model="gpt-3.5-turbo-0125")
dashboard = CropDashboard(llm=llm)

router = APIRouter()


@router.post("/fertilizer_recommendation")
async def get_fertilizer_recommendation(
    farm_data: FarmDataSchema, weather_data: Weather
):
    try:
        fertilizer_chain = dashboard.create_chain(
            prompt_template=FERTILIZER_SYSTEM_PROMPT, structed_output=False
        )
        recommendation = fertilizer_chain.invoke(
            {
                "farm_data": farm_data.model_dump(),
                "weather_data": weather_data.model_dump(),
            }
        )
        return {"recommendation": recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pest_and_disease_control")
async def get_pest_and_disease_control(
    farm_data: FarmDataSchema, weather_data: Weather
):
    try:
        pest_chain = dashboard.create_chain(
            prompt_template=PEST_AND_DISEASE_PROMPT,
            structed_output=True,
            schema=PestDiseaseControlRecommendations,
        )
        control_plan = pest_chain.invoke(
            {
                "farm_data": farm_data.model_dump(),
                "weather_data": weather_data.model_dump(),
            }
        )
        return control_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/weed_control")
async def get_weed_control(farm_data: FarmDataSchema, weather_data: Weather):
    try:
        weed_chain = dashboard.create_chain(
            prompt_template=WEEDS_CONTROL_PROMPT,
            structed_output=True,
            schema=WeedControlRecommendations,
        )
        control_plan = weed_chain.invoke(
            {"farm_data": farm_data.model_dump(), "weather_data": weather_data.model_dump()}
        )
        return control_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/soil_health_and_crop_management")
async def get_soil_health_and_crop_management(
    farm_data: FarmDataSchema, weather_data: Weather
):
    try:
        soil_chain = dashboard.create_chain(
            prompt_template=SOIL_HEALTH_AND_CROP_MANAGEMENT_PROMPT,
            structed_output=True,
            schema=SoilHealthAndCropManagementPlan,
        )
        management_plan = soil_chain.invoke(
            {
                "farm_data": farm_data.model_dump(),
                "weather_data": weather_data.model_dump(),
            }
        )
        return management_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
