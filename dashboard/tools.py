from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

class CustomDDGSearch(DuckDuckGoSearchRun):
   def _run(self, query: str, run_manager: CallbackManagerForToolRun | None = None) -> str:
        results = self.api_wrapper.results(query, max_results=3)
        results = [f"{result['snippet']}\n{result['link']}" for result in results]
        return "\n\n".join(results)


@tool("search_tool", return_direct=True)
def search_tool(query:str):
    """Useful tool to search the web for fertilizer and its application rate, method, and timing\
    disease prevention measures, including application rates, and timing\
    Specific pest control measures including pesticides, application rates, and timing\
    Specific weed control measures, including herbicide with application rate and timing
    """
    ddg = CustomDDGSearch()
    tavily = TavilySearchResults()
    search_engine = tavily.with_fallbacks([ddg])
    results = search_engine.invoke(query)
    if isinstance(results, list):
        results = [f"{result['content']}\n{result['url']}" for result in results]
        results = "\n\n".join(results)
    return results