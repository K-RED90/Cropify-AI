from typing import Any, Coroutine, Type
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_core.pydantic_v1 import BaseModel, Field
from asyncer import asyncify

load_dotenv()


class InputSchema(BaseModel):
    query: str = Field(..., description="The query to the search engine.")

class CustomDDGSearch(DuckDuckGoSearchRun):
    name = "search_engine"
    description = "A search engine tool that retrieves real-time information from the internet for farm-related queries."
    args_schema: Type[BaseModel] = InputSchema
    def _run(
        self, query: str, run_manager: CallbackManagerForToolRun | None = None
    ) -> str:
        results = self.api_wrapper.results(query, max_results=3)
        results = [f"{result['snippet']}\n{result['link']}" for result in results]
        return "\n\n".join(results)

    async def _arun(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, Any]:
        return await asyncify(self._run, cancellable=True)(*args, **kwargs)


@tool("search_engine", return_direct=True, args_schema=InputSchema)
def search_tool(query: str):
    """
    A powerful web search tool designed to retrieve relevant information from the internet for farm-related queries.
    Use this for all farm search queries
    """
    ddg = CustomDDGSearch()
    tavily = TavilySearchResults()
    search_engine = tavily.with_fallbacks([ddg])
    results = search_engine.invoke(query)
    if isinstance(results, list):
        results = [f"{result['content']}\n{result['url']}" for result in results]
        results = "\n\n".join(results)
    return results