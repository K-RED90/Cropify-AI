import React from 'react'
import logo from "../../assets/logo.png"
import {Link} from "react-router-dom"
import "./sidebar.css"
import { FaRocketchat } from "react-icons/fa";
import { AiTwotonePicture } from "react-icons/ai";
import { FaDatabase } from "react-icons/fa";


const Sidebar = () => {
  return (
    <section className='sidebar_div'>
      <div className='logo'>
        <h1>Cropify-AI</h1>
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

      <section className='crop_added'>
        
      </section>

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
    nav: "Chat",
    link: "/",
    icon: <FaRocketchat className='icon'/>
  },
  {
    id:1,
    nav: "Add Farm Data",
    link: "/add-crop",
    icon: <FaDatabase className='icon'/>
  },
  {
    id:2,
    nav: "Add Picture",
    link: "/add-picture",
    icon: <AiTwotonePicture className='icon'/>
  }, 
]

export default Sidebar


