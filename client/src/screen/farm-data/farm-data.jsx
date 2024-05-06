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
        
      </section>
    </DashboardLayout>
  )
}

export default Farm_data
