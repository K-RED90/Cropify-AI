import { createContext, useCallback, useEffect, useState } from "react";
import axios from "axios"


export const farm_data_context = createContext(null)


const Farm_data_provider = ({children}) => {
    
    const [ location, setLocation ] = useState({
        latitude: "",
        longitude:""
    })
    
  const [weather, setWeather] = useState(null)


    const getLocation = useCallback(()=>{
        // Check if Geolocation is supported by the browser
      if ("geolocation" in navigator) {
        // Get current position
        navigator.geolocation.getCurrentPosition(function(position) {
          // Extract latitude and longitude from the position object
          var latitude = position.coords.latitude;
          var longitude = position.coords.longitude;
          
            setLocation({ ...location, longitude: longitude, latitude: latitude })
            
            console.log(location)

        });
      } else {
        // Geolocation is not supported by this browser
        console.log("Geolocation is not supported by this browser.");
      }
},[location, setLocation])

useEffect(()=>{
  getLocation()
}, [])
  
const get_weather = useCallback(async()=>{
  try {
    const response = await axios.get(`http://localhost:8000/weather/weather-by-coordinates/${location.latitude}/${location.longitude}`)
  if (response.status === 200){
    const data = response.data
    setWeather(data)
  }
  } catch (error) {
    console.log(error)
  }
},[location.latitude, location.longitude])
  
  useEffect(() =>{
    if(location.latitude){
      //get_weather()
    }
  },[location.latitude])
  
  if (weather) {
  console.log(weather)
}




  return (
    <farm_data_context.Provider value={{location}}>
      {children}
    </farm_data_context.Provider>
  )
}

export default Farm_data_provider
