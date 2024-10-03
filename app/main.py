from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import os
from app.api.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware
import socket

app = FastAPI()

# Initialize the state variable to store PUUID
app.state.puuid = None

# Include all routes from the router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add the frontend's URL here (Expo default URL)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirect root to /docs
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Function to get the local 192.168.x.x IP address
def get_local_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    if ip_address.startswith('192.168.'):
        return ip_address
    else:
        # Fetch IP from network interfaces if the hostname resolution doesn't return 192.168.x.x
        interfaces = os.popen("ipconfig getifaddr en0").read().strip()
        if interfaces.startswith('192.168.'):
            return interfaces
    return '127.0.0.1'  # Fallback to localhost if no 192.168.x.x IP is found

# Main function to start the server using Uvicorn
def main():
    ip_address = get_local_ip()
    uvicorn.run("app.main:app", host=ip_address, port=8000, reload=True)

if __name__ == "__main__":
    main()
