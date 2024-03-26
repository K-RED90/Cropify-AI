from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal
from langchain_core.prompts import BaseChatPromptTemplate
from langchain_core.language_models import BaseChatModel


class CropDashboard(BaseModel):
    llm: Any
    prompt: Any
    output_parser: Any

    class Config:
        arbitrary_types_allowed = True

    def llm_chain(self):
        chain = self.prompt | self.llm | self.output_parser
        return chain
