from pydantic import BaseModel, Field
import json


class CropSchema(BaseModel):
    crop: str = Field(..., title="Crop Name", description="Name of the crop")
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str):
        return cls.from_dict(json.loads(json_str))