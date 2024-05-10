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
  
   
//   const location = ()=>{
   
//         // Check if Geolocation is supported by the browser
//       if ("geolocation" in navigator) {
//         // Get current position
//         navigator.geolocation.getCurrentPosition(
//     function(position) {
//         // Success callback
//         const latitude = position.coords.latitude;
//         const longitude = position.coords.longitude;
//         console.log("lat:", latitude, "long:", longitude);
//     },
//     function(error) {
//         // Error callback
//         console.error("Error getting location:", error);
//     }
// );
//          console.log("ya")
//       } else {
//         // Geolocation is not supported by this browser
//         console.log("Geolocation is not supported by this browser.");
//       }
//   }
  

//   location()

  if (fertilizer_control) {
    console.log("fert", fertilizer_control)
  }
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
            {fertilizer_control ? (<div>
              <h2>Recommendation</h2>
              <p>{ fertilizer_control?.recommendation}</p>
          </div>): <div>Loading...</div>}
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

export default Control
