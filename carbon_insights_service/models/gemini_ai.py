import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API Key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")  # Correctly initialize the model
    response = model.generate_content(prompt)  # Correct function call
    return response.text  # Extract the response text
