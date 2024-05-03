from typing import Any, Optional, Dict
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.language_models import BaseChatModel
from .utils import load_llm, flatten_nested_dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.messages import HumanMessage
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableParallel,
)
from operator import itemgetter
from logger import log_function_time
from langchain_core.runnables import Runnable, RunnableBranch


class CropDashboard(BaseModel):
    llm: Optional[BaseChatModel] = Field(default_factory=load_llm)

    class Config:
        arbitrary_types_allowed = True

    @log_function_time
    def create_chain(
        self,
        prompt_template,
        structed_output: bool = False,
        schema: BaseModel = None,
    ) -> Runnable:
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = (
            RunnableParallel(
                {
                    "farm_data": itemgetter("farm_data")
                    | RunnableLambda(flatten_nested_dict),
                    "weather_data": itemgetter("weather_data") | RunnablePassthrough(),
                }
            )
            | (lambda x: {**x["farm_data"], **x["weather_data"]})
            | prompt
            | (
                self.llm
                if schema is None
                else self.llm.bind_tools(
                    tools=[convert_to_openai_tool(schema)], tool_choice=schema.__name__
                )
            )
            | (StrOutputParser() if schema is None else JsonOutputToolsParser())
            | RunnableBranch(
                (lambda x: isinstance(x, list), lambda x: x[0]["args"]), (lambda x: x)
            )
        )

        # if structed_output:
        #     if schema is None:
        #         raise ValueError("Schema is required for structured output")
        #     chain = (
        #         base_chain
        #         | (lambda x: [HumanMessage(content=x.content)])
        #         | self.llm.bind_tools(
        #             tools=[convert_to_openai_tool(schema)], tool_choice=schema.__name__
        #         )
        #         | JsonOutputToolsParser()
        #         # | (lambda x: x[0]["args"])
        #     )
        # else:
        #     chain = base_chain | StrOutputParser()
        return chain
