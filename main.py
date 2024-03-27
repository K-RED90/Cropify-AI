from prompts.dashboard import create_prompt
from dashboard.crop_dashboard import CropDashboard
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.output_parsers.fix import OutputFixingParser
from schemas.ai_recommendations import RecommendationsSchema
from typing import Annotated, Sequence
from utils.weather import WeatherAPI
from schemas.farm_data import FarmDataSchema
import os
import json

load_dotenv()

with open(f"sample_data{os.sep}sample.json") as f:
    data = json.load(f)


weather_api = WeatherAPI()


def main(
    data,
    cordinates: Annotated[Sequence[float], "Cordinates of the location (lat, lon)"],
):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-0125",
    )
    # output_parser = JsonOutputToolsParser(strict=True)
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


# if __name__ == "__main__":
#     pprint(main(data, cordinates=(6.6642, -1.8169)))
    # print(token, end="", flush=True)

FarmDataSchema()