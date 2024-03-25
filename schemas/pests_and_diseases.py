from pydantic import BaseModel, Field
from typing import Literal, List, Optional, Dict, Any
import json


class PestsSchema(BaseModel):
    pest_type: Literal["Insect", "Mite", "Nematode", "Rodent", "Bird", "Mammal", "Slug", "Snail", "other"] = Field(..., title="Pest Type", description="Type of pest")
    pest_name: str = Field(..., title="Pest Name", description="Name of the pest")
    damage: str = Field(..., title="Damage", description="Damage caused by the pest")
    symptoms: List[str] = Field(..., title="Symptoms", description="Symptoms of the pest infestation")

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str):
        return cls.from_dict(json.loads(json_str))
    
    class Config:
        schema_extra = {
            "example": {
                "pest_type": "Insect",
                "pest_name": "Aphids",
                "damage": "Sucking sap from plants",
                "symptoms": ["Curling leaves", "Stunted growth", "Honeydew on leaves"],
            }
        }



class DiseasesSchema(BaseModel):
    disease_type: Literal["Fungal", "Bacterial", "Viral", "Nematodal", "Parasitic", "other"] = Field(..., title="Disease Type", description="Type of disease")
    disease_name: str = Field(..., title="Disease Name", description="Name of the disease")
    symptoms: List[str] = Field(..., title="Symptoms", description="Symptoms of the disease")
    spread: str = Field(..., title="Spread", description="How the disease spreads")


    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str):
        return cls.from_dict(json.loads(json_str))
    
    class Config:
        schema_extra = {
            "example": {
                "disease_type": "Fungal",
                "disease_name": "Powdery Mildew",
                "symptoms": ["White powdery growth on leaves", "Yellowing leaves", "Stunted growth"],
                "spread": "Airborne spores",
                "control": "Fungicides, pruning infected parts",
            }
        }

