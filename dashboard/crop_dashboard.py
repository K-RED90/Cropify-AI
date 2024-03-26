from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal, Optional
from langchain_core.prompts import BaseChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool


class CropDashboard(BaseModel):
    llm: Any
    prompt: Any
    output_parser: Any

    class Config:
        arbitrary_types_allowed = True

    def llm_chain(self, tools: Optional[List[BaseTool]] = None):
        if tools is not None:
            tools = [convert_to_openai_tool(tool) for tool in tools]
            # print(tools)
            # import sys; sys.exit()
        else:
            tools = None
        chain = self.prompt | self.llm.bind_tools(tools=tools) | self.output_parser
        return chain
