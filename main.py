from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.traffic_model import TrafficModel
from pydantic import BaseModel
import os

app = FastAPI(title="AI-Powered Traffic Prediction System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "traffic_data.csv")

try:
    model = TrafficModel(DATA_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to initialize model: {e}")

class RouteRequest(BaseModel):
    start_point: str
    destination: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered Traffic Prediction System!"}

@app.post("/predict_routes/")
async def predict_routes(request: RouteRequest):
    start_point = request.start_point.capitalize()
    destination = request.destination.capitalize()

    if not start_point or not destination:
        raise HTTPException(status_code=400, detail="Start point and destination are required.")

    route_options = model.predict_routes(start_point, destination)
    if not route_options:
        raise HTTPException(status_code=404, detail="No routes found for the given start point and destination.")

    return route_options

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
