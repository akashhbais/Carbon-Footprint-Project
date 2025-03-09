from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import certifi

try:
    import google.generativeai as genai
except ModuleNotFoundError:
    raise ImportError("❌ ERROR: 'google.generativeai' module not found. Please install it using 'pip install google-generativeai'.")

from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Ensure SSL works correctly
os.environ["SSL_CERT_FILE"] = certifi.where()

# Load API Key for Gemini AI
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ ERROR: GEMINI_API_KEY not found in .env file!")

genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost:5173",
    "http://10.160.195.20:8000",
    "http://10.160.194.166:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class EmissionRequest(BaseModel):
    company: str
    location: str
    state: str
    date: str
    energyUsage: float
    fuelConsumption: float
    transportDistance: float
    productionQuantity: float
    emissionThreshold: float

@app.get("/ok/")
def get_name():
    return {"message": "API is running"}

@app.post("/calculate-emissions/")
def calculate_emissions(request: EmissionRequest):
    """API to process input fields and generate carbon footprint insights"""

    # ✅ Calculate emissions
    energy_emission = round(request.energyUsage * 0.5, 2)
    fuel_emission = round(request.fuelConsumption * 2.3, 2)
    transport_emission = round(request.transportDistance * 0.15, 2)
    production_emission = round(request.productionQuantity * 0.8, 2)
    total_emission = round(energy_emission + fuel_emission + transport_emission + production_emission, 2)

    # ✅ Compare with threshold
    status = "Above Threshold" if total_emission > request.emissionThreshold else "Below Threshold"
    emission_difference = round(abs(total_emission - request.emissionThreshold), 2)
    percentage_difference = round((emission_difference / request.emissionThreshold) * 100, 2)

    # ✅ CO₂ Reduction Strategies
    solar_reduction = round(energy_emission * 0.3, 2)
    ai_optimized_logistics = round(fuel_emission * 0.1, 2)
    ev_fleet_reduction = round(transport_emission * 0.2, 2)
    energy_efficiency = round(energy_emission * 0.15, 2)

    # ✅ Optimized Resource Utilization
    idle_machine_reduction = round(energy_emission * 0.15, 2)
    fuel_efficiency_savings = round(fuel_emission * 0.1, 2)
    production_optimization = round(production_emission * 0.08, 2)

    # ✅ Generate structured prompt
    prompt = f"""
    You are an AI-powered sustainability expert analyzing carbon emissions data for {request.company} in {request.location}, {request.state}.
    Provide insights in a structured format based on current emissions, resource optimization, and regional trends.

    1️⃣ Current CO₂ Emission Report**
    - Company: {request.company}
    - Location:{request.location}, {request.state}
    - Date: {request.date}
    - Energy Usage: {request.energyUsage} kWh
    - Fuel Consumption: {request.fuelConsumption} Liters
    - Transport Distance: {request.transportDistance} km
    - Total CO₂ Emissions: {total_emission} kg
    - State Emission Threshold: {request.emissionThreshold} kg CO₂
    - Status: {status} ({percentage_difference}% { "higher" if total_emission > request.emissionThreshold else "lower"} than threshold)

    2️⃣ Reduction Strategies
    - Solar Energy Shift (30%): {solar_reduction} kg CO₂ reduction
    - AI-Optimized Logistics (10%): {ai_optimized_logistics} kg CO₂ reduction
    - EV Fleet Adoption (20%): {ev_fleet_reduction} kg CO₂ reduction
    - Energy Efficiency Measures (15%): {energy_efficiency} kg CO₂ reduction

    3️⃣ Optimized Resource Utilization
    - Idle Machine Time Reduction (15%): {idle_machine_reduction} kg CO₂ reduction
    - Route Optimization (10%): {fuel_efficiency_savings} kg CO₂ reduction
    - Smart Scheduling (8%): {production_optimization} kg CO₂ reduction

    4️⃣ Location-wise CO₂ Emissions
    - State:{request.state}
    - City: {request.location}
    - Nearby Average CO₂ Emissions:
        - City 1: {request.emissionThreshold * 1.1} kg CO₂ (Above Threshold)
        - City 2: {request.emissionThreshold * 0.9} kg CO₂ (Below Threshold)
        - City 3: {request.emissionThreshold * 1.05} kg CO₂ (Above Threshold)

    📢 Final Summary
    - CO₂ Emissions Status:{status}
    - Expected Reduction with Strategies: {round(solar_reduction + ai_optimized_logistics + ev_fleet_reduction + energy_efficiency, 2)} kg CO₂
    - Key Recommendations: Implement {["Solar Energy", "EV Fleet", "AI Logistics"][0 if total_emission < request.emissionThreshold else 2]}
    
    Strictly return only this structured response. Avoid adding extra explanations.
    """

    # ✅ Call Gemini AI for response
    gemini_model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    response = gemini_model.generate_content(prompt)

    return {
        "company": request.company,
        "location": request.location,
        "state": request.state,
        "date": request.date,
        "total_emission": f"{total_emission} kg CO₂",
        "status": status,
        "breakdown": {
            "Energy Usage": f"{energy_emission} kg CO₂",
            "Fuel Consumption": f"{fuel_emission} kg CO₂",
            "Transport Distance": f"{transport_emission} kg CO₂",
            "Production Quantity": f"{production_emission} kg CO₂"
        },
        "reduction_strategies": {
            "Solar Energy (30%)": f"{solar_reduction} kg CO₂ reduction",
            "AI-Optimized Logistics (10%)": f"{ai_optimized_logistics} kg CO₂ reduction",
            "EV Fleet (20%)": f"{ev_fleet_reduction} kg CO₂ reduction",
            "Energy Efficiency (15%)": f"{energy_efficiency} kg CO₂ reduction"
        },
        "optimized_utilization": {
            "Idle Machine Reduction (15%)": f"{idle_machine_reduction} kg CO₂ reduction",
            "Route Optimization (10%)": f"{fuel_efficiency_savings} kg CO₂ reduction",
            "Smart Scheduling (8%)": f"{production_optimization} kg CO₂ reduction"
        },
        "regional_emissions": response.text.split("\n")
    }

# ✅ Run FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
