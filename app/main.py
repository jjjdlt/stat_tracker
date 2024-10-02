from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI()

# Initialize the state variable to store PUUID
app.state.puuid = None

# Include all routes from the router
app.include_router(api_router)
