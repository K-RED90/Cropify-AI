from prompts.dashboard import create_prompt
from dashboard.crop_dashboard import CropDashboard
from langchain_openai.chat_models import ChatOpenAI
from langchain_anthropic.chat_models import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import os
import json

load_dotenv()

with open(f"sample_data{os.sep}sample.json") as f:
    data = json.load(f)

def main(data):
    prompt = create_prompt()
    llm = ChatOpenAI(api_key="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")
    output_parser = StrOutputParser()
    dashboard = CropDashboard(llm=llm, prompt=prompt, output_parser=output_parser)
    chain = dashboard.llm_chain()
    for token in chain.stream(data):
        yield token


if __name__ == "__main__":
    for token in main(data):
        print(token, end="", flush=True)