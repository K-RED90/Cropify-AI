from typing import Any, Optional, Dict
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.language_models import BaseChatModel
from .utils import load_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.messages import HumanMessage


class CropDashboard(BaseModel):
    llm: Optional[BaseChatModel] = Field(default_factory=load_llm)
    weather_api: Optional[Any] = None

    class Config:
        arbitrary_types_allowed = True

    def create_chain(
        self,
        farm_data: Dict,
        prompt_template,
        structed_output: bool = False,
        schema: BaseModel = None,
    ):
        prompt = ChatPromptTemplate.from_template(prompt_template)
        base_chain = prompt | self.llm
        if structed_output:
            if schema is None:
                raise ValueError("Schema is required for structured output")
            chain = (
                base_chain
                | (lambda x: [HumanMessage(content=x.content)])
                | self.llm.bind_functions(
                    functions=[convert_to_openai_function(schema)]
                )
                | JsonOutputFunctionsParser()
            )
        else:
            chain = base_chain | StrOutputParser()
        return chain.invoke(farm_data)
