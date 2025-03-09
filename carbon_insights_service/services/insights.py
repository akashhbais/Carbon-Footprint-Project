from models.gemini_ai import get_gemini_response

def generate_insights(co2_transport, co2_warehouse, co2_packaging, industry="logistics"):
    prompt = f"""
    You are an AI sustainability expert specializing in {industry}. 
    Your goal is to analyze the following carbon emissions data and provide industry-specific recommendations:
    
    🌍 **Carbon Emissions Breakdown:**
    - 🚛 Transport CO₂: {co2_transport} kg
    - 🏢 Warehousing CO₂: {co2_warehouse} kg
    - 📦 Packaging CO₂: {co2_packaging} kg
    
    **Your response must include:**
    1️⃣ **Top 3 sustainability actions** specific to the {industry} sector.
    2️⃣ **Estimated CO₂ reduction impact (%)** for each action.
    3️⃣ **Case study examples** from real-world companies using similar strategies.
    4️⃣ **Cost vs. ROI** analysis (low-cost vs. high-impact solutions).
    5️⃣ **Technology-based solutions** (e.g., AI, IoT, renewable energy).
    
    🎯 Provide a structured, concise, and practical recommendation.
    """
    return get_gemini_response(prompt)
