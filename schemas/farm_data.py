import schemas
from pydantic import BaseModel, Field


class FarmDataSchema(BaseModel):
    crop: schemas.CropSchema
    soil: schemas.SoilSchema
    fertilizer: schemas.FertilizerSchema
    pests_and_diseases: schemas.PestsAndDiseasesSchema
    weeds: schemas.WeedControlMeasuresSchema