from pydantic import BaseModel
from typing import List, Any, Optional
from langchain_core.tools import BaseTool
from langchain_core.runnables import RunnableParallel, RunnableLambda
from utils.weather import WeatherAPI
from langchain_core.utils.function_calling import convert_to_openai_tool
import itertools


class CropDashboard(BaseModel):
    llm: Any
    prompt: Any
    output_parser: Any
    fixing_parser: Optional[Any] = None
    weather_api: Any

    class Config:
        arbitrary_types_allowed = True

    def llm_chain(self, tools: Optional[List[BaseTool]] = None):
        if tools is not None:
            tools = [convert_to_openai_tool(tool) for tool in tools]
        else:
            tools = None
        completion_chain = (
            RunnableParallel(
                farm_data=lambda x: x["data"],
                cord=lambda x: self.weather_api.run(x["cordinates"]),
            )
            | RunnableLambda(self._flatten_dict)
            | self.prompt
            | self.llm.bind(tools=tools)
            | self.output_parser
        )
        return completion_chain

    def _flatten_dict(self, data: dict):
        flattened_data = {
            k: v
            for k, v in itertools.chain.from_iterable(
                [value.items() for value in data.values()]
            )
        }
        return flattened_data
