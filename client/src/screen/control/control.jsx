import React, { useContext } from 'react'
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DashboardLayout from '../../components/dashboardLayout/dashboardLayout'
import { farm_data_context } from '../../service/farm_data_context';
import logo from "../../assets/logo.png"
const Control = () => {
    const { 
    fertilizer_control,
    weed_control,
    pests_and_diseases_control,
    soil_crop_management,
  } = useContext(farm_data_context)
  
    const { preventionRecommendations, organicTreatments, chemicalTreatments } = pestDiseaseInfo;
    const { soilHealthRecommendations, integratedCropManagement } = soilCropInfo;
     const { earlyGrowth, midSeason, lateSeason } = weedInfo;
  return (
    <DashboardLayout>
      <div style={{
            width:"95%",
            margin:"auto", 
        }}>
         <div style={{display:"flex", gap:"5px", alignItems:"flex-end", marginTop:"20px", marginLeft:"20px"}}>
           <div style={{width: "30px", height:"30px"}}>
             <img src={ logo} alt='logo' style={{width:"100%", height:"100%", objectFit:"fill"}} />
           </div>
           <small style={{fontSize:"14px"}}>Cropify-AI</small>
         </div>
         
      <Accordion sx={{marginTop:"3rem"}}>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
        >
          <Typography>Fertilizer Recommendations</Typography>
        </AccordionSummary>
        <AccordionDetails sx={{marginLeft:"2rem"}}>
          <Typography>
            {<div>Loading...</div>}
          </Typography>
          
        </AccordionDetails>
      </Accordion>
      
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel2-content"
          id="panel2-header"
        >
          <Typography>Pest and Disease Control</Typography>
        </AccordionSummary>
        <AccordionDetails sx={{marginLeft:"2rem"}}>
        
          {pests_and_diseases_control ? (
            <div>
                <h1>Pest and Disease Control</h1>

                <h2>Prevention Recommendations:</h2>
                <ul>
                {pests_and_diseases_control.prevention_recommendations.map((recommendation, index) => (
                    <li key={index}>{recommendation}</li>
                ))}
                </ul>

                <h2>Organic Treatments:</h2>
                <ul>
                {pests_and_diseases_control.organic_treatments.map((treatment, index) => (
                    <li key={index}>
                    <h4>{treatment.treatment_name}</h4>
                    <ul>
                        <li>Application Rate: {treatment.application_rate}</li>
                        <li>Safety Precautions: {treatment.safety_precautions}</li>
                    </ul>
                    </li>
                ))}
                </ul>

                <h2>Chemical Treatments:</h2>
                {pests_and_diseases_control.chemical_treatments.length === 0 ? (
                <p>No chemical treatments recommended.</p>
                ) : (
                <ul>
                    {pests_and_diseases_control.chemical_treatments.map((treatment, index) => (
                    <li key={index}>{treatment}</li>
                    ))}
                </ul>
                )}
             </div>
          ) : <div>Loading...</div> }
          
        </AccordionDetails>
      </Accordion>
      
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel2-content"
          id="panel2-header"
        >
          <Typography>Weed Control</Typography>
        </AccordionSummary>
        <AccordionDetails sx={{marginLeft:"2rem"}}>
          
          {weed_control ? (
             <div>
                <h1>Weed Management</h1>

                <h2>Early Growth:</h2>
                <h3>Key Weeds:</h3>
                <ul>
                {weed_control.early_growth.key_weeds.map((weed, index) => (
                    <li key={index}>{weed}</li>
                ))}
                </ul>
                <p>Pre-Emergent Herbicides: {weed_control.early_growth.pre_emergent_herbicides}</p>
                <p>Cultural Controls: {weed_control.early_growth.cultural_controls}</p>
                <p>Application Details: {weed_control.early_growth.application_details}</p>

                <h2>Mid-Season:</h2>
                <p>In-Crop Strategies: {weed_control.mid_season.in_crop_strategies}</p>
                <p>Selective Herbicides: {weed_control.mid_season.selective_herbicides}</p>
                <p>Weather Considerations: {weed_control.mid_season.weather_considerations}</p>

                <h2>Late Season:</h2>
                <p>Late-Emerging Weeds: {weed_control.late_season.late_emerging_weeds}</p>
                <p>Desiccants/Harvest Aids: {weed_control.late_season.desiccants_harvest_aids}</p>
                <p>Re-Cropping Concerns: {weed_control.late_season.re_cropping_concerns}</p>
            </div>
          ): <div>Loading...</div>}
          
        </AccordionDetails>
      </Accordion>
      
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel2-content"
          id="panel2-header"
        >
          <Typography>Soil Health and Crop Management</Typography>
        </AccordionSummary>
        <AccordionDetails sx={{marginLeft:"2rem"}}>
          <Typography>
            {}
          </Typography>
          {soil_crop_management ? (
            <div>
                <h1>Soil Health and Crop Management</h1>

                <h2>Soil Health Recommendations:</h2>
                <h3>Soil Amendments:</h3>
                <ul>
                {soil_crop_management.soil_health_recommendations.soil_amendments.map((amendment, index) => (
                    <li key={index}>{amendment}</li>
                ))}
                </ul>

                <h3>Cover Cropping Strategies:</h3>
                <ul>
                {soil_crop_management.soil_health_recommendations.cover_cropping_strategies.map((strategy, index) => (
                    <li key={index}>{strategy}</li>
                ))}
                </ul>

                <h3>Tillage Practices:</h3>
                <ul>
                {soil_crop_management.soil_health_recommendations.tillage_practices.map((practice, index) => (
                    <li key={index}>{practice}</li>
                ))}
                </ul>

                <p>Organic Matter Management: {soil_crop_management.soil_health_recommendations.organic_matter_management}</p>

                <h2>Integrated Crop Management:</h2>
                <p>Irrigation Scheduling: {soil_crop_management.integrated_crop_management.irrigation_scheduling}</p>
                <p>Irrigation Techniques: {soil_crop_management.integrated_crop_management.irrigation_techniques}</p>
                <p>Harvest and Post-Harvest: {soil_crop_management.integrated_crop_management.harvest_and_post_harvest}</p>
            </div>
          ): <div>Loading...</div> }
          
        </AccordionDetails>
      </Accordion>
      
      
    </div>
    </DashboardLayout>
  )
}

const pestDiseaseInfo = {
  preventionRecommendations: [
    "Implement crop rotation with non-host crops to disrupt pest and disease cycles.",
    "Utilize companion planting with pest-repellent plants like marigolds to deter pests naturally.",
    "Incorporate organic mulches to suppress weed growth and create a barrier against pests.",
    "Practice proper irrigation management to avoid water stress and reduce susceptibility to diseases."
  ],
  organicTreatments: [
    {
      "treatment_name": "Neem oil",
      "application_rate": "Dilute 2-4 tablespoons of neem oil in 1 gallon of water and apply as a foliar spray every 7-14 days.",
      "safety_precautions": "Wear protective clothing, avoid contact with eyes, and keep out of reach of children and pets."
    },
    {
      "treatment_name": "Garlic and chili pepper spray",
      "application_rate": "Mix 2-3 cloves of crushed garlic and 1-2 chopped chili peppers in 1 quart of water, let it sit overnight, strain, and spray on plants every 7-10 days.",
      "safety_precautions": "Avoid inhalation of spray mist, wear gloves during preparation and application, and wash hands thoroughly after use."
    }
  ],
  chemicalTreatments: []
};


const soilCropInfo = {
  soilHealthRecommendations: {
    soil_amendments: [
      "Lime to raise pH level",
      "Organic compost for nutrient enrichment"
    ],
    cover_cropping_strategies: [
      "Planting legumes like clover or vetch to fix nitrogen",
      "Growing grasses like ryegrass for soil cover"
    ],
    tillage_practices: [
      "Minimum tillage to reduce soil disturbance",
      "Use of cover crops to minimize erosion"
    ],
    organic_matter_management: "Regular addition of compost and crop residues"
  },
  integratedCropManagement: {
    irrigation_scheduling: "Implement drip irrigation for precise water delivery",
    irrigation_techniques: "Use of mulching to retain soil moisture",
    harvest_and_post_harvest: "Harvest maize at optimal maturity to maximize yield and store in a well-ventilated area"
  }
};


const weedInfo = {
  earlyGrowth: {
    key_weeds: [
      "Palmer amaranth",
      "Giant foxtail",
      "Common lambsquarters"
    ],
    pre_emergent_herbicides: "Atrazine, S-metolachlor",
    cultural_controls: "Hand weeding, crop rotation",
    application_details: "Apply pre-emergent herbicides at a rate of 2.5 L/ha, 2 days before planting. Take precautions to avoid drift and ensure proper calibration of equipment."
  },
  midSeason: {
    in_crop_strategies: "Inter-row cultivation, post-emergent herbicide application",
    selective_herbicides: "Glyphosate, Mesotrione",
    weather_considerations: "Avoid herbicide application during windy conditions or when rain is expected within 24 hours."
  },
  lateSeason: {
    late_emerging_weeds: "Waterhemp, Horseweed",
    desiccants_harvest_aids: "Paraquat, Glyphosate",
    re_cropping_concerns: "Wait 14 days after herbicide application before re-cropping to sensitive crops. Monitor soil pH and organic matter for potential herbicide carryover."
  }
};

export default Control
