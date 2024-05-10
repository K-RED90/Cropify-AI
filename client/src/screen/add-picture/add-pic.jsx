import React from 'react'
import DashboardLayout from '../../components/dashboardLayout/dashboardLayout'
import logo from "../../assets/logo.png"
import "./add-pic.css"
import { Alert, Box, CircularProgress } from '@mui/material'
import { useContext } from 'react'
import { imageContext } from '../../service/image_context'
import ReactMarkdown from 'react-markdown';

const AddPicture = () => {

const {image, get_image, image_response, img_data, pic_loading, img_error, set_img_error, set_pic_loading } = useContext(imageContext)

    // if (img_error) {
    //     const inter = setInterval(() => { 
    //         set_img_error(null)
    //         set_pic_loading(false)
    //     }, [ 2000 ])

    //     return clearInterval(inter)
        
    // }

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
        
        
       {/* {!img_data ? (
             <div style={{width:"100%", display:"flex", justifyContent:"center",  gap:"5px", alignItems:"center", marginTop:"2rem", marginLeft:"20px"}}>
                <div style={{width: "30px", height:"30px"}}>
                    <img src={ logo} alt='logo' style={{width:"100%", height:"100%", objectFit:"fill"}} />
                </div>
                <small style={{fontSize:"14px"}}>Cropify-AI</small>
            </div>
       ) : null} */}
        
        {!img_data ? (
             <div className='content'>
                <h1>Cropify AI's Farm Image Analysis powered by GPT-4V</h1>
                <p>Quickly identify and address crop issues with our powerful 
                arm image analysis tool. Simply upload images of affected
                plants, and our AI system will:
                </p>  
                <ul style={{lineHeight:"16px", fontSize:"16px"}}>
                    <li> ⁠Accurately diagnose diseases, pests, and insect infestations through visual analysis</li>
                    <li><p> ⁠Provide detailed descriptions, symptoms, and potential impact on yields</p></li>
                    <li><p>Perform tailored web searches to find the latest recommended treatments and management strategies</p></li>
                    <li><p>⁠Leverage the cutting-edge GPT-4V language model for precise insights.</p></li>
                </ul> 
                <p>Stay ahead of threats to your crops with Cropify 
                    AI's advanced image analysis capabilities. Detect
                      problems early, get expert guidance on resolutions,
                      and take prompt action for a bountiful harvest 🎉.</p>
            </div>
        ) : null}
        {img_error && (
             <div style={{marginTop:"1rem"}}>
                <Alert  severity="error">{img_error}</Alert>
             </div>
        )}
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
                    <h2>Read more</h2>
                    <ul>
                       {img_data.response_metadata.links.map((link, index)=>{
                        return (
                            <li><a href={link.url}>{ link.title}</a></li>
                            // <ReactMarkdown>{link }</ReactMarkdown>
                        )
                    })} 
                    </ul>
                    
                </div>
            )}
        </div>
    )}
    </DashboardLayout>
  )
}

export default AddPicture
