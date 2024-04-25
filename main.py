from dashboard.crop_dashboard import CropDashboard
from dotenv import load_dotenv
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
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
import tempfile
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from dashboard.schemas.farm_data import FarmDataSchema
from dashboard.weather_tools.get_weather_data import GetWeatherDataByCordinates
from farmGPT.agent_workflow import compile_graph
from langchain_core.runnables import Runnable
from pydantic import BaseModel
from functools import lru_cache
from typing import Optional
import os

load_dotenv(override=True)

app = FastAPI()
dash = CropDashboard()
history = dict()

# In-memory data storage
farm_data: dict[str, FarmDataSchema] = {}
weather_data: Optional[dict] = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# crops_data = {}
# weather_data = {
#     "detail_status": "broken clouds",
#     "reference_time": "2024-04-13T15:52:48+00:00",
#     "sunset_time": "2024-04-13T18:15:13+00:00",
#     "sunrise_time": "2024-04-13T05:59:45+00:00",
#     "wind": "1.59 m/s, direction: 167°",
#     "humidity": "42%",
#     "temperature": "34.7°C",
#     "status": "Clouds",
#     "rain": {},
#     "heat_index": None,
#     "clouds": "63%",
#     "pressure": "1006 hPa",
#     "precipitation_probability": None,
# }


@lru_cache
def load_llm(model_name: str = "gpt-3.5-turbo-0125", temperature: float = 0.5):
    try:
        from langchain_openai.chat_models import ChatOpenAI
    except ImportError:
        raise ImportError(
            "Please install the openai plugin to use the default LLM. Run `pip install langchain-openai`"
        )
    return ChatOpenAI(model=model_name, temperature=temperature)


fertilizer_chain = partial(
    dash.create_chain, prompt_template=FERTILIZER_SYSTEM_PROMPT, structed_output=False
)

pest_chain = partial(
    dash.create_chain,
    prompt_template=PEST_AND_DISEASE_PROMPT,
    structed_output=False,
    schema=PestAndDiseaseControl,
)

weed_chain = partial(
    dash.create_chain,
    prompt_template=WEEDS_CONTROL_PROMPT,
    structed_output=False,
    schema=WeedControlRecommendations,
)

soil_chain = partial(
    dash.create_chain,
    prompt_template=SOIL_HEALTH_AND_CROP_MANAGEMENT_PROMPT,
    structed_output=False,
    schema=SoilHealthAndCropManagementPlan,
)


class WeatherSchema(BaseModel):
    lat: float
    lon: float


@app.get("/")
def read_root():
    return {"message": "Welcome to the Cropify API 🚀"}


@app.post("/data")
def add_farm_data(farm_id: str, data: FarmDataSchema):
    farm_data[farm_id] = data.model_dump()
    return {"message": "Farm data added successfully"}


@app.post("/weather")
def add_weather_data(data: WeatherSchema):
    global weather_data
    weather_data = GetWeatherDataByCordinates().invoke(data.dict())
    return {"message": "Weather data added successfully"}


@app.get("/weather")
def get_weather_data():
    if weather_data is None:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return weather_data


@app.get("/fertilizer/{farm_id}")
def get_fertilizer_recommendations(farm_id: str):
    farm_data_obj = farm_data.get(farm_id)
    if farm_data_obj is None or weather_data is None:
        raise HTTPException(
            status_code=404, detail="Farm data or weather data not found"
        )
    return fertilizer_chain(
        farm_data={"farm_data": farm_data_obj, "weather_data": weather_data}
    )


@app.get("/pest/{farm_id}")
def get_pest_recommendations(farm_id: str):
    farm_data_obj = farm_data.get(farm_id)
    if farm_data_obj is None or weather_data is None:
        raise HTTPException(
            status_code=404, detail="Farm data or weather data not found"
        )
    return pest_chain(
        farm_data={"farm_data": farm_data_obj, "weather_data": weather_data}
    )


@app.get("/weed/{farm_id}")
def get_weed_recommendations(farm_id: str):
    farm_data_obj = farm_data.get(farm_id)
    if farm_data_obj is None or weather_data is None:
        raise HTTPException(
            status_code=404, detail="Farm data or weather data not found"
        )
    return weed_chain(
        farm_data={"farm_data": farm_data_obj, "weather_data": weather_data}
    )


@app.get("/soil/{farm_id}")
def get_soil_recommendations(farm_id: str):
    farm_data_obj = farm_data.get(farm_id)
    if farm_data_obj is None or weather_data is None:
        raise HTTPException(
            status_code=404, detail="Farm data or weather data not found"
        )
    return soil_chain(
        farm_data={"farm_data": farm_data_obj, "weather_data": weather_data}
    )


class Message(BaseModel):
    message: str


def graph(model_name: str = "gpt-3.5-turbo-0125", temperature: float = 0.5):
    try:
        from langchain_openai.chat_models import ChatOpenAI
    except ImportError:
        raise ImportError(
            "Please install the openai plugin to use the default LLM. Run `pip install langchain-openai`"
        )
    llm = ChatOpenAI(model=model_name, temperature=temperature)
    agent = compile_graph(llm=llm)
    return agent


@app.post("/chat/")
async def invoke(request: Message, agent: Runnable = Depends(graph)):
    try:
        return agent.invoke(
            {
                "image_path": None,
                "input": request.message,
                "chat_history": [],
            }
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/image")
async def invoke_with_image(
    image: UploadFile = File(...), agent: Runnable = Depends(graph)
):
    try:
        if image.file:  # Check if image.file is not None
            with tempfile.NamedTemporaryFile(delete=False) as temp_image:
                contents = image.file.read()  # Read the contents
                temp_image.write(contents)
                image_path = temp_image.name
                print(image_path)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No image found"
            )

        output = agent.invoke(
            {
                "image_path": image_path,
                "input": "",
                "chat_history": [],
            }
        )

        if image_path:
            os.remove(image_path)

        return output

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)
