import axios from "axios";
import { createContext, useCallback, useMemo, useState } from "react";
import {nanoid} from "nanoid"


export const chatContext = createContext(null)



const ChatProvider = ({children}) => {
    const [ message, setMessage ] = useState()

    const [ chat, setChat ] = useState([])
    
  const [ chatID, setChatID ] = useState(null)
  const [ chatload, setChatLoad ] = useState(false)
  const [chatError, setChatError] = useState(null)

    const user = "970bc797b7daf89a8523b"

    const get_chat_ID = useCallback(()=>{
        const length = 21

        const randomNanoid = nanoid(length);

        const nanoidLength = randomNanoid.length;
        const randomValues = new Uint32Array(Math.ceil(nanoidLength / 2));
        window.crypto.getRandomValues(randomValues);
        const randomString = Array.from(randomValues, dec => ('0' + dec.toString(16)).substr(-2)).join('').slice(0, nanoidLength);

        console.log("Random string like nanoid:", randomString);
        setChatID(randomString)
    }, [])
    
    const get_screen_message = async (mes)=>{
        setChatLoad(true)
      try {
          setMessage(mes)
          const chat_response = await axios.post(`http://localhost:5000/farmGPT/chat`, { message: mes, user_id:user, conversation_id:chatID })
          setChatLoad(false)
          if (chat_response.status === 200) {
            const data = await chat_response.data.content
        setChat([...chat, {user:mes, ai:data, links:chat_response?.data?.response_metadata?.links ? chat_response?.data?.response_metadata?.links : []}])
      }
        } catch (error) {
          setChatError(error.message)
        }
    }

  const get_input_message = (e)=>{
    setMessage(e.target.value)
  }

 const button_sent = async ()=>{
   setChatLoad(true)
   try {
       
       const chat_response = await axios.post(`http://localhost:5000/farmGPT/chat`, { message: message, user_id:user, conversation_id:chatID })
      
      if (chat_response.status === 200) {
        const data = await chat_response.data.content
        setChat([ ...chat, { user: message, ai: data, links:chat_response?.data?.response_metadata?.links ? chat_response?.data?.response_metadata?.links : [] } ])
        setChatLoad(false)
      }
    } catch (error) {
      setChatError(error.message)
    }
    } 

  return (
      <chatContext.Provider value={{
          get_screen_message,
          get_chat_ID,
          chat,
          chatload,
          get_input_message,
          button_sent,
          chatError,
          setChatError,
          setChatLoad
      }}>
      {children}
    </chatContext.Provider>
  )
}

export default ChatProvider
