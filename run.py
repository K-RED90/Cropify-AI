from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from farm.endpoints import router as farm_router
from weather.endpoints import router as weather_router


app = FastAPI()
app.include_router(farm_router, prefix="/farm")
app.include_router(weather_router, prefix="/weather")

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

    uvicorn.run(app, host="localhost", port=8000)