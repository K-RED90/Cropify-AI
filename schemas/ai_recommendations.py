from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal


class AIRecommend(BaseModel):
    pests_control: List[str] = Field(..., title="Pests Control", description="4 for controlling pests")
    diseases_control: List[str] = Field(..., title="Diseases Control", description="4 for controlling diseases")