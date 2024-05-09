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
            <p>🌱 Cropify AI: Your Intelligent Farming Companion 🌾
            Welcome to Cropify AI, the cutting-edge agricultural solution that harnesses the power of artificial intelligence to revolutionize your farming experience! 🚀
            With our three innovative features, we empower you to unlock the full potential of your crops and maximize your yields like never before.
              </p>
          </div>
          <button onClick={()=>navigation()}>Try Cropify AI</button>
        </div>
        <div className='right'>
          <img src={img} alt='imag'/>
        </div>
      </section>
      </section>
      
      <div style={{
        width: "80%",
        margin: "auto",
        marginBottom:"6rem"
      }}>
        <div>
          <h1 style={{borderBottom:"1px solid black", padding:"10px", marginTop:"5rem",}}>Purpose of Cropify-AI</h1>
        </div>

        <ol>
          <li><h2>AgriScan</h2></li>
            <p>Diagnose Crop Issues with AI Image Analysis
            Simply upload images of your affected plants,
            and our advanced AI system, powered by GPT-4V,
            will accurately identify diseases, pests, and insect infestations.
            Get detailed descriptions, potential impacts, and recommended treatments
            – all at your fingertips! 🌿</p>
          
          <li><h2>AgroAssist</h2></li>
              <p>Your Virtual Farm Advisor
                Engage in natural conversations with our intelligent chatbot, 
                AgroAssist. Leveraging weather tools and search engines, it provides
                expert guidance on crop cultivation, pest management, and farming best
                practices. Plus, it shares valuable links for further reading! 🌍
              </p>
            
          <li><h2>AgriAdvisor</h2></li>
            <p>
              Data-Driven Farm Management
              By analyzing your farm data, such as crop types, soil
              conditions, and real-time weather information, AgriAdvisor delivers
              tailored recommendations for optimizing fertilizer application,
              pest control, soil health, and crop management. Maximize your yields
              with data-driven insights! 📈
            </p>
        </ol>
      </div>

      <div style={{width:"100%", height:"40vh", backgroundColor:"#325757", display: "flex", flexDirection:"column", justifyContent:"center", alignItems:"center", color:"white"}}>
        <h1>Join the future of intelligent agriculture with Cropify AI! </h1>
        <p>Embrace our cutting-edge technology and transform your farming operations into a sustainable, efficient, and prosperous venture.
          ower of AI in agriculture today! 🌐</p>
      </div>
    </div>
  )
}

export default Homepage
