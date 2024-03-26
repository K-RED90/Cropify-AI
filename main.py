from prompts.dashboard import create_prompt
from dashboard.crop_dashboard import CropDashboard
from langchain_openai.chat_models import ChatOpenAI
from langchain_anthropic.chat_models import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from schemas.ai_recommendations import Recommendations, FertilizerUse, PestControl, DiseaseControl, WeedSuppression
import os
import json

load_dotenv()

with open(f"sample_data{os.sep}sample.json") as f:
    data = json.load(f)

def main(data):
    prompt = create_prompt()
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key="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")
    output_parser = JsonOutputToolsParser(strict=True)
    dashboard = CropDashboard(llm=llm, prompt=prompt, output_parser=output_parser)
    chain = dashboard.llm_chain(tools=[Recommendations])
    return chain.invoke(data)
        # yield token


if __name__ == "__main__":
    print(main(data))
        # print(token, end="", flush=True)