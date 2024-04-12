from dashboard.crop_dashboard import CropDashboard
from dotenv import load_dotenv
import json
from dashboard.prompt_templates import (
    FERTILIZER_SYSTEM_PROMPT,
    PEST_AND_DISEASE_PROMPT,
    WEEDS_CONTROL_PROMPT,
    SOIL_HEALTH_AND_CROP_MANAGEMENT_PROMPT,
)
from dashboard.schemas.ai_recommendations import (
    PestAndDiseaseControl,
    WeedControlRecommendations,
    SoilHealthAndCropManagementPlan,
)
from functools import partial
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dashboard.schemas.farm_data import FarmDataSchema
from dashboard.weather_tools.get_weather_data import GetWeatherDataByCordinates


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv(override=True)

crops_data = {}
weather_data = None
dash = CropDashboard()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Cropify API 🚀"}


@app.post("/data")
def add_farm_data(farm_id, data: FarmDataSchema):
    crops_data[farm_id] = data.model_dump()
    return {"message": "Farm data added successfully"}


# Add weather data
@app.post("/weather")
def add_weather_data(data: dict):
    global weather_data
    weather_data = data
    return {"message": "Weather data added successfully"}


@app.get("/weather")
def get_weather_data():
    return weather_data


# fertilizer_chain = partial(dash.chain_with_structured_output, FERTILIZER_SYSTEM_PROMPT, FertilizerSchema)
@app.get("/pest")
def get_pest_recommendations(farm_id):
    pest_chain = partial(
        dash.create_chain,
        prompt_template=PEST_AND_DISEASE_PROMPT,
        schema=PestAndDiseaseControl,
        structed_output=True,
    )
    farmer_and_weather_data = {**crops_data[farm_id], **weather_data}
    print(farmer_and_weather_data)


fertilizer_chain = partial(
    dash.create_chain, prompt_template=FERTILIZER_SYSTEM_PROMPT, structed_output=False
)
weed_chain = partial(
    dash.create_chain,
    prompt_template=WEEDS_CONTROL_PROMPT,
    schema=WeedControlRecommendations,
    structed_output=True,
)
soil_chain = partial(
    dash.create_chain,
    prompt_template=SOIL_HEALTH_AND_CROP_MANAGEMENT_PROMPT,
    schema=SoilHealthAndCropManagementPlan,
    structed_output=True,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)