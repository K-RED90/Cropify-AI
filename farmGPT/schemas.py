from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import List, Optional, Literal


class ResponseFormat(BaseModel):
    """
    Use this schema to format the response to the user's query.
    """

    answer: str = Field(
        ..., description="A clear and concise answer to the user's query."
    )
    links: List[str] = Field(
        ...,
        description="A list of relevant links in markdown format to support the answer. Eg. [Link Title](URL).",
    )


class SearchQuery(BaseModel):
    """
    Pydantic model for a single search query.
    """

    query: str = Field(..., description="The search query string.")


class SearchQueryOutput(BaseModel):
    """
    Pydantic model for the output of generating search queries based on a farmer's query.
    """

    farmer_query: str = Field(
        ..., description="The original farm query posed by the farmer."
    )

    search_queries: List[SearchQuery] = Field(
        ...,
        description="A list of 1-3 focused search queries to find relevant information to address the farmer's query.",
    )


class AnswerEvaluation(BaseModel):
    """
    Pydantic model for evaluating an AI-generated answer to a farmer's query.
    """

    evaluation: Literal[
        "complete",
        "partially_complete",
    ] = Field(
        ...,
        description="The assessment of whether the AI answer addresses the farmer's query.",
    )
    feedback: Optional[str] = Field(
        None,
        description="Feedback on missing or inaccurate information if the evaluation is 'Partially answers the query'.",
    )

    @validator("feedback", always=True)
    def validate_feedback(cls, feedback, values):
        evaluation = values.get("evaluation")
        if evaluation == "partially_complete" and not feedback:
            raise ValueError(
                "Feedback is required if the evaluation is 'Partially answers the query'."
            )
        return feedback


class AnswerRefinement(BaseModel):
    """
    Pydantic model for refining a previous AI-generated answer to a farmer's query.
    """

    answer: str = Field(
        ...,
        description="The updated and refined answer incorporating the feedback and additional information.",
    )
