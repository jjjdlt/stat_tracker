from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from app.api.routes import router as api_router

app = FastAPI()

# Initialize the state variable to store PUUID
app.state.puuid = None

# Include all routes from the router
app.include_router(api_router)

# Redirect root to /docs
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Main function to start the server using Uvicorn
def main():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
