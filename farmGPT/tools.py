from typing import Any, Coroutine
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_core.pydantic_v1 import BaseModel, Field
from asyncer import asyncify

load_dotenv()


class CustomDDGSearch(DuckDuckGoSearchRun):
    def _run(
        self, query: str, run_manager: CallbackManagerForToolRun | None = None
    ) -> str:
        results = self.api_wrapper.results(query, max_results=3)
        results = [f"{result['snippet']}\n{result['link']}" for result in results]
        return "\n\n".join(results)

    def _arun(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, Any]:
        return asyncify(self._run, cancellable=True)(*args, **kwargs)


class InputSchema(BaseModel):
    query: str = Field(..., description="The query to the search engine.")


@tool("search_tool", return_direct=True, args_schema=InputSchema)
def search_tool(query: str):
    """Useful tool to search the web for farm-related queries."""
    ddg = CustomDDGSearch()
    tavily = TavilySearchResults()
    search_engine = tavily.with_fallbacks([ddg])
    results = search_engine.invoke(query)
    if isinstance(results, list):
        results = [f"{result['content']}\n{result['url']}" for result in results]
        results = "\n\n".join(results)
    return results