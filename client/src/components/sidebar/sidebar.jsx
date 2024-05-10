import React from 'react'
import logo from "../../assets/logo.png"
import {Link} from "react-router-dom"
import "./sidebar.css"
import { FaRocketchat } from "react-icons/fa";
import { AiTwotonePicture } from "react-icons/ai";
import { FaDatabase } from "react-icons/fa";
import { WiHumidity } from "react-icons/wi";
import { CiTempHigh } from "react-icons/ci";


const Sidebar = () => {
  const url  = window.location.pathname

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

      {url !== "/dashboard/farm-data" && (<section className='crop_added'>
        
      </section>)}
      
      {url === "/dashboard/farm-data" && (
        <section className='weather_box' style={{paddingLeft:"2rem", fontSize:"14px" }}>
          <div style={{display:"flex", lineHeight:"1px", gap:"4rem", justifyContent:"flex-start", alignItems:"center"}} className='box'>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", alignItems:"center",  lineHeight:"1px"}}>
              <WiHumidity style={{fontSize:"25px"}}/>
              <p>Humidity</p>
            </div>
            <p>75%</p>
          </div>
          <div style={{display:"flex", lineHeight:"1px", gap:"4rem", justifyContent:"flex-start", alignItems:"center"}} className='box'>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", alignItems:"center",  lineHeight:"1px"}}>
              <CiTempHigh style={{fontSize:"25px"}}/>
              <p>Temperature</p>
            </div>
            <p>75%</p>
          </div>
          <div style={{display:"flex", lineHeight:"1px", gap:"4rem", justifyContent:"flex-start", alignItems:"center"}} className='box'>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", alignItems:"center",  lineHeight:"1px"}}>
              <WiHumidity style={{fontSize:"25px"}}/>
              <p>Humidity</p>
            </div>
            <p>75%</p>
          </div>
          <div style={{display:"flex", lineHeight:"1px", gap:"4rem", justifyContent:"flex-start", alignItems:"center"}} className='box'>
            <div style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", alignItems:"center",  lineHeight:"1px"}}>
              <WiHumidity style={{fontSize:"25px"}}/>
              <p>Humidity</p>
            </div>
            <p>75%</p>
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


