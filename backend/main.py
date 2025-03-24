import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import google.generativeai as genai
import re
import uuid

# Load API Key
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("❌ Error: GEMINI_API_KEY is missing! Please set it in your .env file.")

genai.configure(api_key=API_KEY)

try:
    models = genai.list_models()
    available_models = [model.name for model in models if "gemini" in model.name]
    

    PREFERRED_MODEL = "models/gemini-2.0-flash-thinking-exp-01-21"
    model_name = PREFERRED_MODEL if PREFERRED_MODEL in available_models else available_models[0] if available_models else None

except Exception as e:
    print(f"❌ Error fetching models: {e}")
    model_name = None

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Dictionary to store chat history with unique chat IDs
chats = {}

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chats": chats})

@app.post("/chat")
async def chat(user_query: str = Form(...), chat_id: str = Form(...)):
    global chats

    if not model_name:
        return JSONResponse({"error": "❌ No valid Gemini model available."}, status_code=500)

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(user_query)
        bot_response = response.text if hasattr(response, "text") else "⚠ No valid response from AI."

        # ✅ Ensure only headings and subheadings are bold
        bot_response = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", bot_response)  # Bold only for headings
        bot_response = re.sub(r"\* (.*?)", r"• \1", bot_response)  # Bullet points

        if chat_id not in chats:
            chats[chat_id] = {"title": user_query[:30], "messages": []}

        chats[chat_id]["messages"].append({"user": user_query, "bot": bot_response})

        return JSONResponse({"chat_id": chat_id, "user": user_query, "bot": bot_response})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
