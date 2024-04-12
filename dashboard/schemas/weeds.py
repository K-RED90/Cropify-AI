from pydantic import BaseModel, Field
from typing import Literal


class WeedControlMeasuresSchema(BaseModel):
    method: Literal["chemical", "biological", "mechanical", "cultural"] = Field(description="Method of weed control")
    frequency: Literal["Once", "Twice", "Thrice", "Four times", "More than four times"] = Field(title="Frequency", description="Number of times the weed control measure is applied in a year")
