from prompts.dashboard import create_prompt
from dashboard.crop_dashboard import CropDashboard
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.output_parsers.fix import OutputFixingParser
from schemas.ai_recommendations import RecommendationsSchema
from typing import Annotated, Sequence, Any
from utils.weather import WeatherAPI
from fastapi import FastAPI
from schemas.farm_data import FarmDataSchema
from pprint import pprint

import os
import json

load_dotenv()

with open(f"sample_data{os.sep}sample.json") as f:
    data = json.load(f)


weather_api = WeatherAPI()
database = {}


def main(
    data,
    cordinates: Annotated[Sequence[float], "Cordinates of the location (lat, lon)"],
):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-0125",
    )
    output_parser, format_instructions = RecommendationsSchema.get_format_instructions()
    fixing_parser = OutputFixingParser.from_llm(llm=llm, parser=output_parser)
    fixing_parser.parse_with_prompt
    prompt = create_prompt()
    prompt = prompt.partial(format_instructions=format_instructions)
    dashboard = CropDashboard(
        llm=llm,
        prompt=prompt,
        output_parser=output_parser,
        fixing_parser=fixing_parser,
        weather_api=weather_api,
    )

    chain = dashboard.llm_chain()
    return chain.invoke(input={"data": data, "cordinates": cordinates})


app = FastAPI()

@app.post("/cropt")
def add_crop(id: Any, data: FarmDataSchema):
    database[id] = data.model_dump()
    return {"message": "Crop added successfully"}

@app.get("/crop/{id}")
def get_crop(id: Any):
    return database[id]

@app.post("/crop/{id}/recommendations")
def get_recommendations(id: Any, cordinates: Annotated[Sequence[float], "Cordinates of the location (lat, lon)"]):
    return main(data = database[id], cordinates=cordinates)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)