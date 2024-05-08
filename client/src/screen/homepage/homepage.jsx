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
          <h1 style={{color:"white", fontSize:"30px"}}>
            Cropify-AI:
          </h1>
          <div className='strong'>
            Revolutionizing Farming with Artificial Intelligence
          </div>

          <div className='technology'>
            Our AI platform is here to support you in every aspect of crop management. While our system is advanced, we understand that mistakes can happen. That's why we've implemented rigorous checks on critical information to ensure accuracy.
            Whether you're chatting with us, snapping photos of your crops, or providing farm data, rest assured that our AI carefully verifies important details before offering recommendations. We're committed to providing reliable guidance to help you optimize crop yield and ensure a healthy harvest.
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
