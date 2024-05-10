import { createContext, useCallback, useEffect, useState } from "react";
import axios from "axios"


export const farm_data_context = createContext(null)


const Farm_data_provider = ({children}) => {
    
    const [ location, setLocation ] = useState({
        latitude: "",
        longitude:"",
    })
  
  const [location_name, set_location_name] = useState(null)
    
  const [ weather, setWeather ] = useState({})
  
  const [ farm_data, set_farm_data ] = useState({
    soil_type: "",
    soil_ph: "",
    crop: "",
    pct_soil_moisture: "",
    soil_fertility: "",
    diseases: "",
    pests: ""
  })
  
  const [ soil_crop_management, set_soil_crop_management] = useState(null)
  const [ fertilizer_control, set_fertilizer_control ] = useState("")
  const [ weed_control, set_weed_control ] = useState(null)
  const [ pests_and_diseases_control, set_pests_and_diseases_control ] = useState(null)
  const [ error, setError ] = useState([])
  const [load, setLoad] = useState(false)
  const [nav, setNav] = useState(false)



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
    const response = await axios.get(`http://localhost:5000/weather/weather-by-coordinates/${location.latitude}/${location.longitude}`)
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
      get_weather()
    }
  },[location])
  
  if (weather) {
  console.log(weather)
}

const get_loaction_name = async()=>{
 try {
     const response = await axios.get(`http://localhost:5000/weather/current-location/${location.latitude}/${location.longitude}`)

   if (response.status === 200) {
     const data = await response.data.location[0].name
     set_location_name(data)
  }
 } catch (error) {
  console.log(error)
 }
}
  
  useEffect(()=>{
    if (location.latitude) {
      get_loaction_name()
    }
  }, [location])

  if (location_name) {
    console.log("location", location_name)
  }
  
  
const get_farm_data = useCallback((e) =>{
  set_farm_data({ ...farm_data, [ e.target.name ]: e.target.value })
  // set_fertilizer_control(null)
  // set_weed_control(null)
  // set_pests_and_diseases_control(null)
  // soil_and_crop_management_response(null)
  setNav(false)
  console.log(farm_data)
}, [farm_data])


  const fertilizer_data_response = async ()=>{
    console.log("click")
    try {
      const farm_body = {
        farm_data: {
          crop: farm_data.crop,
          soil: {
            soil_type: farm_data.soil_type,
            soil_ph: farm_data.soil_ph,
            pct_soil_moisture: farm_data.pct_soil_moisture,
            soil_fertility: farm_data.soil_fertility
          },
      pests_and_diseases: {
        diseases: farm_data.diseases,
        pests: farm_data.pests
      }
        },
        weather_data: {
          status: weather?.status,
          wind: weather?.wind,
          humidity: weather?.humidity,
          temperature: weather?.temperature,
          heat_index: weather?.heat_index,
          clouds: weather?.clouds,
          pressure: weather?.pressure,
          precipitation_probability: weather?.precipitation_probability
        }
      }
      const fertilizer_response = await axios.post(`http://localhost:5000/farm/fertilizer_recommendation`, farm_body)
      console.log(farm_body)
      if (fertilizer_response.status === 200) {
        const data = await fertilizer_response.data 
        set_fertilizer_control(data)
      }

    } catch (err) {
      setError([...error, err.message])
    }
  }

   const weed_data_response = async ()=>{
    console.log("click")
    try {
      const farm_body = {
        farm_data: {
          crop: farm_data.crop,
          soil: {
            soil_type: farm_data.soil_type,
            soil_ph: farm_data.soil_ph,
            pct_soil_moisture: farm_data.pct_soil_moisture,
            soil_fertility: farm_data.soil_fertility
          },
      pests_and_diseases: {
        diseases: farm_data.diseases,
        pests: farm_data.pests
      }
        },
        weather_data: {
          status: weather?.status,
          wind: weather?.wind,
          humidity: weather?.humidity,
          temperature: weather?.temperature,
          heat_index: weather?.heat_index,
          clouds: weather?.clouds,
          pressure: weather?.pressure,
          precipitation_probability: weather?.precipitation_probability
        }
      }
      setNav(false)
      const fertilizer_response = await axios.post(`http://localhost:5000/farm/weed_control`, farm_body)
      
      if (fertilizer_response.status === 200) {
        const data = await fertilizer_response.data 
        set_weed_control(data)
        console.log(data)
        setNav(true)
      }

    } catch (err) {
      setError([...error, err.message])
    }
   }
  
   const pests_and_diseases_response = async ()=>{
    console.log("click")
    try {
      const farm_body = {
        farm_data: {
          crop: farm_data.crop,
          soil: {
            soil_type: farm_data.soil_type,
            soil_ph: farm_data.soil_ph,
            pct_soil_moisture: farm_data.pct_soil_moisture,
            soil_fertility: farm_data.soil_fertility
          },
      pests_and_diseases: {
        diseases: farm_data.diseases,
        pests: farm_data.pests
      }
        },
        weather_data: {
          status: weather?.status,
          wind: weather?.wind,
          humidity: weather?.humidity,
          temperature: weather?.temperature,
          heat_index: weather?.heat_index,
          clouds: weather?.clouds,
          pressure: weather?.pressure,
          precipitation_probability: weather?.precipitation_probability
        }
      }
      setLoad(true)
      setNav(false)
      const fertilizer_response = await axios.post(`http://localhost:5000/farm/pest_and_disease_control`, farm_body)
      
      if (fertilizer_response.status === 200) {
        const data = await fertilizer_response.data 
        set_pests_and_diseases_control(data)
        setNav(true)
        setLoad(false)
      }

    } catch (err) {
      setError([...error, err.message])
    }
   }
  
  const soil_and_crop_management_response = async ()=>{
    console.log("click")
    try {
      const farm_body = {
        farm_data: {
          crop: farm_data.crop,
          soil: {
            soil_type: farm_data.soil_type,
            soil_ph: farm_data.soil_ph,
            pct_soil_moisture: farm_data.pct_soil_moisture,
            soil_fertility: farm_data.soil_fertility
          },
      pests_and_diseases: {
        diseases: farm_data.diseases,
        pests: farm_data.pests
      }
        },
        weather_data: {
          status: weather?.status,
          wind: weather?.wind,
          humidity: weather?.humidity,
          temperature: weather?.temperature,
          heat_index: weather?.heat_index,
          clouds: weather?.clouds,
          pressure: weather?.pressure,
          precipitation_probability: weather?.precipitation_probability
        }
      }
      setNav(false)
      const fertilizer_response = await axios.post(`http://localhost:5000/farm/soil_health_and_crop_management`, farm_body)
      
      if (fertilizer_response.status === 200) {
        const data = await fertilizer_response.data 
        set_soil_crop_management(data)
        setNav(true)
      }

    } catch (err) {
      setError([...error, err.message ])
    }
  }
  return (
    <farm_data_context.Provider value={{
      location,
      get_farm_data,
      fertilizer_data_response,
      fertilizer_control,
      weed_data_response,
      weed_control,
      pests_and_diseases_response,
      pests_and_diseases_control,
      soil_and_crop_management_response,
      soil_crop_management,
      error,
      load,
      setLoad,
      nav,
      setError,
      weather,
      location_name
      }}>
      {children}
    </farm_data_context.Provider>
  )
}

export default Farm_data_provider


