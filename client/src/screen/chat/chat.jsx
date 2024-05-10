import React, { useEffect } from 'react'
import DashboardLayout from "../../components/dashboardLayout/dashboardLayout"
import logo from "../../assets/logo.png"
import "./chat.css"
import { Alert, Box, Button, CircularProgress } from '@mui/material'
import { IoIosSend } from "react-icons/io";
import { FaRegArrowAltCircleUp } from "react-icons/fa";
import ReactMarkdown from 'react-markdown';
import { useContext } from 'react'
import { chatContext } from '../../service/chat_context'
import { FaArrowDownLong } from "react-icons/fa6";
const Chat = () => {
  const { get_screen_message, get_chat_ID , chat, get_input_message, button_sent, chatload, chatError, setChatError, setChatLoad} = useContext(chatContext)
  
  useEffect(()=>{
    get_chat_ID()
  }, [])

   if (chatError) {
        const inter = setInterval(() => { 
            setChatError(null)
          setChatLoad(false)
        return clearInterval(inter)
        }, [ 2000 ])
        
    }

  const scroll = ()=>{
    const divElement = document.getElementById('chat');
    
    // Scroll the div to the bottom
    if (divElement) {
      divElement.scrollTop = divElement.scrollHeight
    }
 }
  
   scroll()

 console.log("Load", chatload)
  return (
    <DashboardLayout>
      <section className='chat_ai'>
         <div style={{display:"flex", gap:"5px", alignItems:"flex-end", marginTop:"20px", marginLeft:"20px"}}>
           <div style={{width: "30px", height:"30px"}}>
             <img src={ logo} alt='logo' style={{width:"100%", height:"100%", objectFit:"fill"}} />
           </div>
           <small style={{fontSize:"14px"}}>Cropify-AI</small>
         </div>
         
        {chatError && (
           <div style={{marginTop:"1rem"}}>
                <Alert  severity="error">{chatError}</Alert>
          </div>
        )}
        {chat.length > 0 && (
           <div className='chat_box' id="chat">
             {chat.map((chat, index)=>{
               return (
                <div  key={"index"} className='messages'>
                  <div className='user_message'>
                    <div className='circle'>You</div>
                    <div className='message'> {chat.user}</div>
                  </div>
                  <div className='ai_message'>
                    <div className='circle'>AI</div>
                     <div className='message'>
                       
                       <ReactMarkdown>{chat.ai}</ReactMarkdown>
                       {chat.links.length > 0 && <h3>Read more</h3>}
                       {chat.links && (
                         <ul>
                           {chat.links.map((link, index)=>{
                            return (
                              <li><a href={link.url}>{link.title}</a></li>
                              // <ReactMarkdown key={index}>{link}</ReactMarkdown>
                            )
                          })}
                         </ul>
                       )}
                       
                    </div>
                  </div>
                </div>
              )
             })}
        </div>
        )}
       
        {!chatload && chat.length > 2 && (
          <div style={{lineHeight:"2px", fontSize:"12px", width:"80%", display:"flex", flexDirection:"column", justifyContent:"center", alignItems:"center", margin:"auto"}}>
            <FaArrowDownLong />
            <p>Scroll</p>
          </div>
        )}

        {
          chatload && (
                      <div style={{display:"flex", justifyContent:"center", alignItems:"center", width:"100%"}}>
           <Box  sx={{ display: 'flex'}}>
              <CircularProgress />
            </Box> 
        </div>

          )
        }

        
        <section className='question_and_input'>
          {chat.length === 0 && (
            <div className='question'>

            {
              question.map((question, index)=>{
                return (
                   <div key={question.id} className='question_box' onClick={()=>get_screen_message(question.message)}>
                    <div className='ques_content'>
                      <p className='bold'>{question.ques}</p>
                      <p className='hint'>{ question.hint}</p>
                    </div>
                    <div className='send_quetion'>
                      <FaRegArrowAltCircleUp className='message_icon' />
                    </div>
                  </div>
                )
              })
            }
          </div>
         )}
          
          <div className='input'>
            <section className='input_area'>
              <textarea
                contenteditable="true"
                placeholder="Type your farm or weather query here..."
                className='input_field'
                onChange={get_input_message}
              />
              <Button variant='contained' sx={{ width: "10%", height: "40px", padding: "10px", color: "white", backgroundColor: "#325757", borderRadius:"12px" }} onClick={()=>button_sent()}>
                <IoIosSend  className='send'/>
              </Button>
            </section>
            <div style={{textAlign:"center", width:"100%", fontSize:"14px", fontWeight:"lighter"}}>"Powered by ChatGPT, I'm here to help you grow better. Ask me anything about farming!"</div>
          </div>
        </section>
      </section>
    </DashboardLayout>
  )
}


const question = [
  {
    id: 0,
    ques: 'The current temperature and weather conditions in Cape Coast?',
    message: "What are the current temperature and weather conditions in Cape Coast?",
    hint:"As an AI I can provide you your current weather condition and temperature"
  },
  {
    id: 1,
    ques: '⁠What crop rotation techniques benefit soil health in tropical regions such as Northern Ghana?',
    message: " ⁠What crop rotation techniques benefit soil health in tropical regions such as Northern Ghana?",
    hint:"Let me show you the Beneficts of crop lotation techniques"
  },
  {
    id: 2,
    ques: ` ⁠Check Kumasi's forecast next week for rain that could affect apple orchard pesticide spraying.`,
    message: ` ⁠Check Kumasi's forecast next week for rain that could affect apple orchard pesticide spraying.`,
    hint:"let me predicKumasi's forecast next week for rain that could affect apple orchard pesticide spraying."
  },
  {
    id: 3,
    ques: 'What are effective organic or natural methods for controlling tomato hornworm infestations?',
    message: "What are effective organic or natural methods for controlling tomato hornworm infestations?",
    hint:"The effective organic or natural methods for controlling tomato hornworm infestations "
  },
  
  
]

export default Chat
