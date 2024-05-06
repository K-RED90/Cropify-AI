import React from 'react'
import logo from "../../assets/logo.png"
import "./sidebar.css"
const Sidebar = () => {
  return (
    <section className='sidebar'>
      <div className='logo'>
        <div className='logo_image'>
          <img src={ logo} alt='logo'  />
        </div>
        <h3>Cropify-AI</h3>
      </div>
    </section>
  )
}

export default Sidebar


