import { createContext, useCallback, useEffect, useState } from "react";
import axios from "axios"
export const farm_data_context = createContext(null)


const Farm_data_provider = ({children}) => {
    
    const [ location, setLocation ] = useState({
        latitude: "",
        longitude:""
    })


    const getLocation = useCallback(()=>{
        // Check if Geolocation is supported by the browser
      if ("geolocation" in navigator) {
        // Get current position
        navigator.geolocation.getCurrentPosition(function(position) {
          // Extract latitude and longitude from the position object
          var latitude = position.coords.latitude;
          var longitude = position.coords.longitude;
          
            setLocation({ ...location, llongitude: longitude, latitude: latitude })
            
            console.log(location)

        });
      } else {
        // Geolocation is not supported by this browser
        console.log("Geolocation is not supported by this browser.");
      }
},[location, setLocation])

const get_weather = async ()=>{
    try {
        const response = await axios.get(`/current-location/${location.latitude}/${location.longitude}`)
    } catch (error) {
        
    }
    
}


  return (
    <farm_data_context.Provider value={{}}>
      {children}
    </farm_data_context.Provider>
  )
}

export default Farm_data_provider
