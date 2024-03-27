import schemas
from pydantic import BaseModel, Field


class FarmDataSchema(BaseModel):
    crop: schemas.CropSchema
    soil: schemas.SoilSchema
    fertilizer: schemas.FertilizerSchema
    pests: schemas.PestsSchema
    diseases: schemas.DiseasesSchema
    weeds: schemas.WeedControlMeasuresSchema