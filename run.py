from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv(override=True)
from farm.endpoints import router as farm_router
from weather.endpoints import router as weather_router
from farmGPT.endpoints import router as farmGPT_router


app = FastAPI()
app.include_router(farm_router, prefix="/farm")
app.include_router(weather_router, prefix="/weather")
app.include_router(farmGPT_router, prefix="/farmGPT")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, "0.0.0.0")
