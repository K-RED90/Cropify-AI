import React, { useContext } from 'react'
import logo from "../../assets/logo.png"
import {Link} from "react-router-dom"
import "./sidebar.css"
import { FaRocketchat } from "react-icons/fa";
import { AiTwotonePicture } from "react-icons/ai";
import { FaDatabase } from "react-icons/fa";
import { WiHumidity } from "react-icons/wi";
import { CiTempHigh } from "react-icons/ci";
import { MdWindPower } from "react-icons/md";
import { GiPressureCooker } from "react-icons/gi";
import { SiInstatus } from "react-icons/si";
import { farm_data_context } from '../../service/farm_data_context';



const Sidebar = () => {
  const url  = window.location.pathname
  const { weather, location_name } = useContext(farm_data_context)
  
  return (
    <section className='sidebar_div'>
      <div className='logo'>
        <Link to="/" style={{textDecoration:"none", color:"white"}}><h1>Cropify-AI</h1></Link>
      </div>

      <nav className='nav'>
        {
          data?.map(nav =>{
            const url = `/dashboard${nav.link}`
              return (
              <Link style={{textDecoration:"none", color:"white"}} to={url} key={nav.id} className='nav_container'>
                <div style={{TextDecoder:"none"}}>
                  {nav.icon}
                  <p className='chat'>{ nav.nav}</p>
                </div>
              </Link>
          )
          } )
        }
      </nav>

      {/* {!url && (<section className='crop_added'>
        
     </section>)} */}
      
      {weather && (
         <section className='weather_box' style={{ paddingLeft: "1rem", fontSize: "14px", borderRadius: "8px",  paddingTop:"5px", paddingBottom:"5px", paddingRight:"10px"}}>
          <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex_start", width:"100%", gap:"1.2rem"}}>
            <h3 style={{width:"30%"}}> Weather</h3>
            <p style={{fontSize:"18px", width:"70%", fontWeight:700}}>{location_name}</p>
          </div>
          <div style={{display:"flex", lineHeight:"1px", gap:"4rem", justifyContent:"flex-start", alignItems:"center"}} className='box'>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", alignItems:"flex-start",  lineHeight:"1px", width:"60%"}}>
              <SiInstatus style={{fontSize:"25px"}}/>
              <p>Status</p>
            </div>
            <p style={{ width: "40%" }}>{ weather.status}</p>
          </div>
          <div style={{display:"flex", lineHeight:"1px", gap:"4rem", justifyContent:"flex-start", alignItems:"center"}} className='box'>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", alignItems:"flex-start",  lineHeight:"1px", width:"60%"}}>
              <CiTempHigh style={{fontSize:"25px"}}/>
              <p>Temperature</p>
            </div>
            <p style={{ width: "40%" }}>{ weather.temperature}</p>
          </div>
          <div style={{display:"flex", lineHeight:"1px", gap:"4rem", justifyContent:"flex-start", alignItems:"center"}} className='box'>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", alignItems:"flex-start",  lineHeight:"1px", width:"60%"}}>
              < MdWindPower style={{fontSize:"25px"}}/>
              <p>Wind</p>
            </div>
            <p style={{ width: "40%" }}>{weather?.wind?.split(",")[0] }</p>
          </div>
          <div style={{display:"flex", lineHeight:"1px", gap:"4rem", justifyContent:"flex-start", alignItems:"center"}} className='box'>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", alignItems:"flex-start",  lineHeight:"1px", width:"60%"}}>
              < GiPressureCooker style={{fontSize:"25px"}}/>
              <p>Pressure</p>
            </div>
            <p style={{ width: "40%" }}>{ weather.pressure}</p>
          </div>
        </section>
       )}
        
      <section className='user'>
          <div className='user_circle'>N</div>
          <h1 className='name'>Nicolas</h1>
      </section>

    </section>
  )
}

const data = [
  {
    id:0,
    nav: "AgroAssist",
    link: "/",
    icon: <FaRocketchat className='icon'/>
  },
  {
    id:2,
    nav: "AgriScan",
    link: "/image",
    icon: <AiTwotonePicture className='icon'/>
  }, 
  {
    id:1,
    nav: "AgriAdvisor",
    link: "/farm-data",
    icon: <FaDatabase className='icon'/>
  },
  
]

export default Sidebar


