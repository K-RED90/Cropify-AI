import React, { useEffect } from 'react'
import DashboardLayout from "../../components/dashboardLayout/dashboardLayout"
import logo from "../../assets/logo.png"
import "./chat.css"
import { Button } from '@mui/material'
import { IoIosSend } from "react-icons/io";
import { FaRegArrowAltCircleUp } from "react-icons/fa";
import ReactMarkdown from 'react-markdown';
import { useContext } from 'react'
import { chatContext } from '../../service/chat_context'
const Chat = () => {
  const { get_screen_message, get_chat_ID } = useContext(chatContext)
  
  useEffect(()=>{
    get_chat_ID()
  }, [])
  return (
    <DashboardLayout>
      <section className='chat_ai'>
         <div style={{display:"flex", gap:"5px", alignItems:"flex-end", marginTop:"20px", marginLeft:"20px"}}>
           <div style={{width: "30px", height:"30px"}}>
             <img src={ logo} alt='logo' style={{width:"100%", height:"100%", objectFit:"fill"}} />
           </div>
           <small style={{fontSize:"14px"}}>Cropify-AI</small>
         </div>
         
        {/* <div className='chat_box'>
             <div  key={"index"} className='messages'>
                <div className='user_message'>
                  <div className='circle'>You</div>
                  <div className='message'> {"chat.user"}</div>
                </div>
                <div className='ai_message'>
                  <div className='circle'>AI</div>
                  <div className='message'>
                    <ReactMarkdown>{ "chat.chat"}</ReactMarkdown>
                  </div>
                </div>
              </div>
        </div> */}

        <section className='question_and_input'>
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

          <div className='input'>
            <section className='input_area'>
              <textarea
                contenteditable="true"
                placeholder="Provide a message related to farming and weather..."
                className='input_field'
                // onChange={getMessage}
              />
              <Button variant='contained' sx={{ width: "10%", height: "50px", padding: "10px", color: "white", backgroundColor: "#325757", borderRadius:"12px" }}>
                <IoIosSend  className='send'/>
              </Button>
            </section>
            <div style={{textAlign:"center", width:"100%", fontSize:"14px", fontWeight:"lighter"}}>Cropify-Ai can make mistakes. Consider checking important information.</div>
          </div>
        </section>
      </section>
    </DashboardLayout>
  )
}


const question = [
  {
    id: 0,
    ques: 'Help me get my current weather ?',
    message: "what is my current weather",
    hint:"As an AI I can provide you your current weather condition"
  },
  {
    id: 1,
    ques: 'Is farming help economic growth ?',
    message: "does farming promote economy ?",
    hint:"Let me show you the Beneficts of farming"
  },
  {
    id: 2,
    ques: 'Will it rain today ?',
    message: "will it be raining today ?",
    hint:"I can predict if it will be raining today"
  },
  {
    id: 3,
    ques: 'How to start farming ?',
    message: "can you teach me how I can start farming ?",
    hint:"Farming is important let me quide you how to start"
  },
  
  
]

export default Chat
