import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import google.generativeai as genai

# Load API Key from .env file
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Fetch available models
try:
    models = genai.list_models()
    available_models = [model.name for model in models if "gemini" in model.name]
    print("✅ Available Gemini Models:", available_models)
    
    # Choose the best available model
    PREFERRED_MODEL = "models/gemini-1.5-flash-002"
    if PREFERRED_MODEL in available_models:
        model_name = PREFERRED_MODEL
    elif available_models:
        model_name = available_models[0]  # Fallback to first available
    else:
        model_name = None

except Exception as e:
    print(f"❌ Error fetching models: {e}")
    model_name = None

# Initialize FastAPI app
app = FastAPI()

# Set up Jinja2 templates
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def chat(request: Request, user_query: str = Form(...)):
    if not model_name:
        return {"response": "❌ Error: No valid Gemini model available."}

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(user_query)
        bot_response = response.text if hasattr(response, "text") else "No response from Gemini."
    except Exception as e:
        bot_response = f"❌ Error: {str(e)}"

    return {"response": bot_response}
