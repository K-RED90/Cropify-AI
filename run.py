from dashboard.crop_dashboard import CropDashboard
from dotenv import load_dotenv
import json
from dashboard.prompt_templates import FERTILIZER_SYSTEM_PROMPT, PEST_AND_DISEASE_PROMPT, WEEDS_CONTROL_PROMPT, SOIL_HEALTH_AND_CROP_MANAGEMENT_PROMPT
from dashboard.schemas.ai_recommendations import PestAndDiseaseControl, WeedControlRecommendations, SoilHealthAndCropManagementPlan
from functools import partial

load_dotenv(override=True)

with open(r"sample_data\sample.json") as f:
    farm_data = json.load(f)


dash = CropDashboard()
# fertilizer_chain = partial(dash.chain_with_structured_output, FERTILIZER_SYSTEM_PROMPT, FertilizerSchema)
pest_chain = partial(dash.create_chain, prompt_template=PEST_AND_DISEASE_PROMPT, schema=PestAndDiseaseControl, structed_output=True)
fertilizer_chain = partial(dash.create_chain, prompt_template=FERTILIZER_SYSTEM_PROMPT, structed_output=False)
weed_chain = partial(dash.create_chain, prompt_template=WEEDS_CONTROL_PROMPT, schema=WeedControlRecommendations, structed_output=True)
soil_chain = partial(dash.create_chain, prompt_template=SOIL_HEALTH_AND_CROP_MANAGEMENT_PROMPT, schema=SoilHealthAndCropManagementPlan, structed_output=True)
print(soil_chain(farm_data))

