from .fertilizer import FertilizerSchema
from .pests_and_diseases import PestsAndDiseasesSchema
from .soil import SoilSchema
from pydantic import BaseModel, Field


class FarmDataSchema(BaseModel):
    crop: str = Field(description="Name of the crop")
    soil: SoilSchema
    # fertilizer: FertilizerSchema
    pests_and_diseases: PestsAndDiseasesSchema