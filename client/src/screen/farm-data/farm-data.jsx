import React, { useContext } from 'react'
import DashboardLayout from '../../components/dashboardLayout/dashboardLayout'
import "./farm-data.css"
import { farm_data_context } from '../../service/farm_data_context'
const Farm_data = () =>
{
  const { location } = useContext(farm_data_context)
  
  console.log(location)
  return (
    <DashboardLayout>
      <section className='farm_data'>
        <div className='weather'>

        </div>

        <section className='data_field'>
          <h1>Provide farm data</h1>
            <form>
              <div className='crop'>
                <h3 for="crop">Crop</h3>
                <div className='crop_field'>
                  <input type='text' name='crop' id='crop' placeholder='Enter crop'/>
                </div>
              </div>
              
            <div className='soil'>
              <h3>Soil</h3>
              <div className='soil_container'>

                {
                  solidData?.map((data, index) => {
                    return (
                      <div className='soil_field' key={data.id}>
                        <label for={data.name}>{ data.lable}</label>
                        <select id={data.name} name={data.name}>
                          <option value="">Select</option>
                          {
                            data.option.map((option, i)=>{
                              return <option key={option.id} value={option.value} >{ option.value}</option>
                            })
                          }
                            
                            
                        </select>
                      </div>
                    )
                  })
                }
                
                  <div className='pct_soil_moisture'>
                    <label htmlFor="pct_soil_moisture">Percentage soil moisture</label>
                    <div className='pct_soil_moisture_field'>
                      <input type='text' name='pct_soil_moisture' placeholder='Enter the percentage of the soil moisture'/>
                    </div>
                  </div>
              </div>
            </div>
            
            <div className='pests_and_diseases'>
              <h3>Pests and Diseases</h3>
               <div>
                  <div className='field'>
                      <input type='text' name='pest' placeholder='Enter pests '/>
                  </div>
                  <div className='field'>
                      <input type='text' name='diseases' placeholder='Enter Diseases'/>
                  </div>
               </div>
            </div>

          </form>

          <div>
            <button>Submit</button>
          </div>
        </section>
        
      </section>
    </DashboardLayout>
  )
}


const solidData = [
  {
    id: 0,
    lable: "Soil type",
    name: "soil_type",
    option: [
      {
        id: 0,
        value:"Clay"
      },
      {
        id: 1,
        value:"Sandy"
      },
      {
        id: 2,
        value:"Loamy"
      },
      {
        id: 3,
        value:"Chalky"
      },
      {
        id: 4,
        value:"Silt"
      },
    ]
  },

  {
    id: 1,
    lable: "Soil PH",
    name: "soil_ph",
    option: [
      {
        id: 0,
        value:"Strong acidic (3.5–4.4)"
      },
      {
        id: 1,
        value:"Acidic (4.5-6.5)"
      },
      {
        id: 2,
        value:"Neutral (6.6–7.3)"
      },
      {
        id: 3,
        value:"Alkaline (7.4-9)"
      },
      {
        id: 4,
        value:"Strongly alkaline: > 9.0"
      },
    ]
  },
  {
    id: 2,
    lable: "Soil Fertility",
    name: "soil_fertility",
    option: [
      {
        id: 0,
        value:"Low"
      },
      {
        id: 1,
        value:"Medium"
      },
      {
        id: 2,
        value:"High"
      },
    ]
  },
]

export default Farm_data
