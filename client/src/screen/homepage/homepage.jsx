import React from 'react'

import "./homepage.css"
import img from "../../assets/img.png"
import logo from "../../assets/logo.png"

import { useNavigate } from 'react-router-dom'


const Homepage = () => {
    
    const navigate = useNavigate()
     const navigation = ()=>{
        navigate("/dashboard")
    }

  return (
    <div>
      <section className='home'>
      <section className='header'>
        <div className='logo'>
          <h1>Cropify-AI</h1>
          <div className='image'>
            <img src={logo } alt='logo' />
          </div>
        </div>
        <button onClick={()=>navigation()}>Try Cropify AI</button>
      </section>
      <section className='body'>
        <div className='left'>
          <strong>
            Cropify-AI:
          </strong>
          <div className='strong'>
            Revolutionizing Farming with Artificial Intelligence
          </div>

          <div className='technology'>
            Technology has revolutionized modern agriculture, making farming more efficient, sustainable, and productive while enabling farmers to meet the growing demand for food in a changing world.
          </div>
          <button onClick={()=>navigation()}>Try Cropify AI</button>
        </div>
        <div className='right'>
          <img src={img} alt='imag'/>
        </div>
      </section>
     </section>
    </div>
  )
}

export default Homepage
