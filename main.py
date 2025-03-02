

# # main.py
# from fastapi import FastAPI, HTTPException
# from models.traffic_model import TrafficModel
# from pydantic import BaseModel
# import os

# app = FastAPI(title="AI-Powered Traffic Prediction System")

# # Configuration
# DATA_PATH = os.getenv("TRAFFIC_DATA_PATH", "data/traffic_data.csv")

# # Initialize model
# try:
#     model = TrafficModel(DATA_PATH)
# except Exception as e:
#     raise RuntimeError(f"Failed to initialize model: {e}")

# # Request model for API input
# class RouteRequest(BaseModel):
#     start_point: str
#     destination: str

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the AI-Powered Traffic Prediction System!"}

# @app.post("/predict_routes/")
# async def predict_routes(request: RouteRequest):
#     """API endpoint to predict routes."""
#     start_point = request.start_point.capitalize()
#     destination = request.destination.capitalize()

#     # Validate input
#     if not start_point or not destination:
#         raise HTTPException(status_code=400, detail="Start point and destination are required.")

#     # Get route predictions
#     route_options = model.predict_routes(start_point, destination)
#     if not route_options:
#         raise HTTPException(status_code=404, detail="No routes found for the given start point and destination.")

#     return route_options

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from models.traffic_model import TrafficModel
from pydantic import BaseModel
import os

app = FastAPI(title="AI-Powered Traffic Prediction System")

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Configuration
DATA_PATH = os.getenv("TRAFFIC_DATA_PATH", "data/traffic_data.csv")

# Initialize model
try:
    model = TrafficModel(DATA_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to initialize model: {e}")

# Request model for API input
class RouteRequest(BaseModel):
    start_point: str
    destination: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered Traffic Prediction System!"}

@app.post("/predict_routes/")
async def predict_routes(request: RouteRequest):
    """API endpoint to predict routes."""
    start_point = request.start_point.capitalize()
    destination = request.destination.capitalize()

    # Validate input
    if not start_point or not destination:
        raise HTTPException(status_code=400, detail="Start point and destination are required.")

    # Get route predictions
    route_options = model.predict_routes(start_point, destination)
    if not route_options:
        raise HTTPException(status_code=404, detail="No routes found for the given start point and destination.")

    return route_options

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)