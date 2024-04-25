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
import os

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
weather_data = {
    "detail_status": "broken clouds",
    "reference_time": "2024-04-13T15:52:48+00:00",
    "sunset_time": "2024-04-13T18:15:13+00:00",
    "sunrise_time": "2024-04-13T05:59:45+00:00",
    "wind": "1.59 m/s, direction: 167°",
    "humidity": "42%",
    "temperature": "34.7°C",
    "status": "Clouds",
    "rain": {},
    "heat_index": None,
    "clouds": "63%",
    "pressure": "1006 hPa",
    "precipitation_probability": None,
}
dash = CropDashboard()

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

history = dict()


def load_llm(model_name: str = "gpt-3.5-turbo-0125", temperature: float = 0.5):
    try:
        from langchain_openai.chat_models import ChatOpenAI
    except ImportError:
        raise ImportError(
            "Please install the openai plugin to use the default LLM. Run `pip install langchain-openai`"
        )
    return ChatOpenAI(model=model_name, temperature=temperature)


# class Message(BaseModel):
#     input: str
#     session_id: str = uuid4()


# def load_conversation_history(session_id: str = uuid4()):
#     if session_id not in history:
#         history[session_id] = ChatMessageHistory()
#     return history[session_id]


# @app.post("/compile")
# def compile_agent_workflow(llm: BaseChatModel = Depends(load_llm)):
#     try:
#         global agent
#         agent = RunnableWithMessageHistory(
#             runnable=compile_graph(llm=llm),
#             input_messages_key="input",
#             history_messages_key="chat_history",
#             get_session_history=load_conversation_history,
#         )
#         return {"message": "Agent workflow compiled successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Welcome to the Cropify API 🚀"}


@app.post("/data")
def add_farm_data(farm_id, data: FarmDataSchema):
    crops_data[farm_id] = data.model_dump()
    return {"message": "Farm data added successfully"}


class WeatherSchema(BaseModel):
    lat: float
    lon: float


# Add weather data
@app.post("/weather")
def add_weather_data(data: WeatherSchema):
    global weather_data
    weather_data = GetWeatherDataByCordinates().invoke(data.model_dump())
    return {"message": "Weather data added successfully"}


@app.get("/weather")
def get_weather_data():
    return weather_data


@app.get("/fertilizer")
def get_fertilizer_recommendations(farm_id):
    return fertilizer_chain(
        farm_data={"farm_data": crops_data[farm_id], "weather_data": weather_data}
    )


@app.get("/pest")
def get_pest_recommendations(farm_id):
    pest_chain = partial(
        dash.create_chain,
        prompt_template=PEST_AND_DISEASE_PROMPT,
        schema=PestAndDiseaseControl,
        structed_output=True,
    )
    return pest_chain(
        farm_data={"farm_data": crops_data[farm_id], "weather_data": weather_data}
    )


@app.get("/weed")
def get_weed_recommendations(farm_id):
    return weed_chain(
        farm_data={"farm_data": crops_data[farm_id], "weather_data": weather_data}
    )


@app.get("/soil")
def get_soil_recommendations(farm_id):
    return soil_chain(
        farm_data={"farm_data": crops_data[farm_id], "weather_data": weather_data}
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
