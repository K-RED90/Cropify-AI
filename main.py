from prompts.dashboard import create_prompt
from dashboard.crop_dashboard import CropDashboard
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langchain.output_parsers.fix import OutputFixingParser
from schemas.ai_recommendations import RecommendationsSchema
import os
import json

load_dotenv()

with open(f"sample_data{os.sep}sample.json") as f:
    data = json.load(f)


def main(data):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-0125",
        api_key="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",
    )
    # output_parser = JsonOutputToolsParser(strict=True)
    output_parser, format_instructions = RecommendationsSchema.get_format_instructions()
    fixing_parser = OutputFixingParser.from_llm(llm=llm, parser=output_parser)
    fixing_parser.parse_with_prompt
    prompt = create_prompt()
    prompt = prompt.partial(format_instructions=format_instructions)
    dashboard = CropDashboard(
        llm=llm, prompt=prompt, 
        output_parser=output_parser, 
        fixing_parser=fixing_parser
    )

    chain = dashboard.llm_chain(tools=None)
    return chain.invoke(data)
    # yield token


if __name__ == "__main__":
    print(main(data))
    # print(token, end="", flush=True)
