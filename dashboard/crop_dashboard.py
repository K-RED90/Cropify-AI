from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal, Optional
from langchain_core.prompts import BaseChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.runnables import RunnableParallel, RunnableLambda


class CropDashboard(BaseModel):
    llm: Any
    prompt: Any
    output_parser: Any
    fixing_parser: Optional[Any] = None

    class Config:
        arbitrary_types_allowed = True

    def llm_chain(self, tools: Optional[List[BaseTool]] = None):
        # if tools is not None:
        #     tools = [convert_to_openai_tool(tool) for tool in tools]
        #     # print(tools)
        #     # import sys; sys.exit()
        # else:
        #     tools = None
        completion_chain = self.prompt | self.llm | self.output_parser
        # main_chain = RunnableParallel(
        #     completion=completion_chain, prompt=self.prompt
        # ) | RunnableLambda(lambda x: self.fixing_parser.parse_with_prompt(**x))
        return completion_chain
