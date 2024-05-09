import axios from "axios";
import { createContext, useState } from "react";

export const imageContext = createContext(null)


const ImageProvider = ({children}) => {
    const [ image, setImage ] = useState("")
    const [ picture, setPicture ] = useState(null)
    
    const [ img_data, set_img_data ] = useState(null)
    const [ img_error, set_img_error ] = useState(null)
    const [ pic_loading, set_pic_loading ] = useState(false)

    
    const get_image = (e)=>{
        setPicture(e.target.files[ 0 ])
        if (e.target.files && e.target.files[0]) {
        setImage(URL.createObjectURL(e.target.files[0]));
        }
    }

    const image_response = async()=>{
        const formData = new FormData();
        formData.append('image', picture);
        try {
            if (picture) {
                set_pic_loading(true)
                const response = await axios.post(`http://localhost:5000/farmGPT/image`, formData)
                if (response.status === 200) {
                    const data = await response.data
                    set_img_data(data)
                    set_pic_loading(false)
                }
            } else {
                alert("Upload image")
            }
        } catch (error) {
           set_img_error(error.message)
        }
    }

  return (
    <imageContext.Provider value={{image, get_image, image_response, img_data, pic_loading, img_error, set_img_error,set_pic_loading }}>
      {children}
    </imageContext.Provider>
  )
}

export default ImageProvider
