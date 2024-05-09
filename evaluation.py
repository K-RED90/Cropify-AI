import asyncio
import json
import re
import time
from glob import glob
from pathlib import Path
from dotenv import load_dotenv
from farmGPT.agent_workflow import compile_graph
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_groq.chat_models import ChatGroq
from models import load_llm
from typing import Literal

load_dotenv(override=True)


EVALUATION_PROMPT = """
You are an agricultural expert tasked with evaluating the performance of an AI model designed to identify diseases, pests, and insects from images.

The model will provide a prediction, and you will compare it with the actual label.

When evaluating the predictions, you should:

1. Disregard any spelling mistakes or minor variations in the predicted and actual labels.
2. Consider alternative names or synonyms for the diseases, pests, and insects.

For example, if the predicted label is "Corn Earworm" and the actual label is "Earworm on Corn," you should respond with "Y" since they refer to the same thing, despite the slight variation in wording.

Prediction: {prediction}
Actual Label: {actual_label}
"""


class ImageEvaluator:
    def __init__(self, image_dir="./example_images"):
        self.image_dir = image_dir
        self.model = load_llm(model="gpt-3.5-turbo-0125")
        self.chain = (
            compile_graph(llm=self.model)
            | (lambda x: x.content)
            | RunnableLambda(self.extract_name)
        )
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.eval_chain = self.prompt | ChatGroq(
            model="Llama3-70b-8192", temperature=0
        ).with_structured_output(Evaluation)
        self.full_chain = {
            "prediction": self.chain,
            "actual_label": RunnablePassthrough(),
        } | self.eval_chain
        self.template = EVALUATION_PROMPT

    def get_image_files(self):
        return [
            {
                "image_path": image,
                "messages": [],
                "chat_history": [],
                "actual_label": Path(image).stem.split("_")[0],
            }
            for image in glob(f"{self.image_dir}/*")
        ]

    def extract_name(self, text):
        for category in ["Pest", "Disease"]:
            pattern = rf"\*\*{category}\*\*: (.*?)\n\n"
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None

    async def evaluate_images(self, batch_size=2, sleep_time=60):
        image_files = self.get_image_files()
        score = []
        for i in range(0, len(image_files), batch_size):
            batch = image_files[i : i + batch_size]
            output = await self.full_chain.abatch(batch, config={"max_concurrency": 2})
            score.extend([item.dict() for item in output])
            if i + batch_size < len(image_files):
                time.sleep(sleep_time)
        return score

    def save_scores(self, scores, filename="./score.json"):
        with open(filename, "w") as f:
            json.dump(scores, f, indent=4)


class Evaluation(BaseModel):
    """Use this tool to evaluate the performance of an AI model designed to identify diseases, pests, and insects from images."""

    evaluation: Literal["Y", "N"] = Field(
        ...,
        description="Evaluation of the prediction. Reply with 'Y' if the prediction is accurate, and 'N' if it is inaccurate.",
    )
    prediction: str = Field(..., description="The predicted label.")
    actual_label: str = Field(..., description="The actual label.")


if __name__ == "__main__":
    evaluator = ImageEvaluator()
    scores = asyncio.run(evaluator.evaluate_images())
    evaluator.save_scores(scores)
