import React from 'react'
import DashboardLayout from '../../components/dashboardLayout/dashboardLayout'
import logo from "../../assets/logo.png"
import "./add-pic.css"
import { Box, CircularProgress } from '@mui/material'
import { useContext } from 'react'
import { imageContext } from '../../service/image_context'
import ReactMarkdown from 'react-markdown';

const AddPicture = () => {

const {image, get_image, image_response, img_data, pic_loading } = useContext(imageContext)

const open =()=>{
    document.getElementById("file").click()
}
    
  return (
    <DashboardLayout>
       <div style={{display:"flex", gap:"5px", alignItems:"flex-end", marginTop:"20px", marginLeft:"20px"}}>
           <div style={{width: "30px", height:"30px"}}>
             <img src={ logo} alt='logo' style={{width:"100%", height:"100%", objectFit:"fill"}} />
           </div>
           <small style={{fontSize:"14px"}}>Cropify-AI</small>
        </div>
        
        <div className='image'>
            <div className='upload_container'>
                <div>
                    <div className='upload_box'>
                        <p onClickCapture={()=>open()}>Browse image</p> 
                    </div>
                    <input type='file' id='file' style={{display:"none"}} onChange={get_image}/>
                    <button className='upload_btn' onClick={()=> image_response ()} >Upload</button>
                </div>
               {
                image && (
                     <div className='image_box'>
                        <img src={image} alt='pic'/>
                    </div>
                )
               }
            </div>
        </div>
        
        
       {!img_data ? (
             <div style={{width:"100%", display:"flex", justifyContent:"center",  gap:"5px", alignItems:"center", marginTop:"2rem", marginLeft:"20px"}}>
                <div style={{width: "30px", height:"30px"}}>
                    <img src={ logo} alt='logo' style={{width:"100%", height:"100%", objectFit:"fill"}} />
                </div>
                <small style={{fontSize:"14px"}}>Cropify-AI</small>
            </div>
       ) : null}
        
        {!img_data ? (
             <div className='content'>
                <h1>Empower your farming endeavors with our AI-powered solution</h1>
                <p>Simply provide images of your crops affected by pests or diseases,
                    and receive personalized recommendations instantly. Our ready-to-use
                    components are free forever, offering you a seamless experience in managing
                    your farm's health. With accessibility always in mind, our platform provides
                    invaluable assistance for optimizing crop yield and ensuring a healthy harvest.
                </p>   
            </div>
        ) : null}
    
          {
              pic_loading && (
                <div className='loading'>
                    <Box  sx={{ display: 'flex'}}>
                        <CircularProgress />
                    </Box>  
                </div>
              )
          }
    
    {img_data && (
        <div className='data_content'>
            <ReactMarkdown>
                {img_data.content}
            </ReactMarkdown>
            
            {img_data.response_metadata.links && (
                <div>
                    <h2>Links</h2>
                    {img_data.response_metadata.links.map((link, index)=>{
                        return (
                            <ReactMarkdown>{link }</ReactMarkdown>
                        )
                    })}
                </div>
            )}
        </div>
    )}
    </DashboardLayout>
  )
}

export default AddPicture
