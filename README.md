# LLM Chatbot App  

A FastAPI-based chatbot using Google Gemini AI with a responsive frontend.

## 📁 Project Structure  
     
     llm-app/ │── backend/ │ │── templates/ │ │ │── index.html # Frontend UI (HTML + JS) │ │── main.py # FastAPI backend │ │── .env # Stores API key │ │── requirements.txt # Python dependencies │── .gitignore # Ignore unnecessary files │── README.md # Documentation



## 🚀 Features  
- Interactive chatbot with Google Gemini AI  
- FastAPI backend & Jinja2 templating  
- Chat history support with unique session IDs  
- Minimalistic dark-themed UI  

## 📌 Installation  
```sh
git clone https://github.com/your-username/llm-app.git
cd llm-app/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

Create .env in backend/ and add:
    GEMINI_API_KEY=your_google_gemini_api_key


Run the server:
    uvicorn main:app --reload

📌 Usage
  Open http://127.0.0.1:8000/ in your browser.
  Start chatting with the AI.
  Click New Chat to reset the conversation.

🛠 Tech Stack
   Backend: FastAPI, Google Generative AI
   Frontend: HTML, JavaScript, Jinja2
   Styling: CSS (Dark Theme)
