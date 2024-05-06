import React from 'react'
import "./dashboardLayout.css"
import Sidebar from "../sidebar/sidebar"
const DashboardLayout = ({children}) => {
  return (
    <div className='layout'>
      <div className="sidebar">
        <Sidebar/>
      </div>

      <div className="children">
        {children}
      </div>
    </div>
  )
}

export default DashboardLayout
