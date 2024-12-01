from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import openai
from dotenv import load_dotenv
import os

# Memuat file .env
load_dotenv()

# Mengambil API key dari .env
api_key = os.getenv("OPENAI_API_KEY")

# Menetapkan API key untuk OpenAI
openai.api_key = api_key  # Pastikan API key digunakan di OpenAI

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Konfigurasi template rendering
templates = Jinja2Templates(directory="templates")

# Endpoint untuk menampilkan halaman utama
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint untuk halaman chat
@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

# Endpoint untuk menangani form submission dari HTML
@app.post("/chat")
async def chat_with_gpt4(request: Request, user_message: str = Form(...)):
    try:
        # Panggilan ke OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Menggunakan model GPT-3.5 Turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{user_message}"}
            ],
            max_tokens=100,  # Jumlah token output
            temperature=0.7  # Mengontrol kreativitas output
        )
        
        bot_message = response['choices'][0]['message']['content'].strip()
        return templates.TemplateResponse("chat.html", {"request": request, "user_message": user_message, "bot_response": bot_message})

    except Exception as e:
        return templates.TemplateResponse("chat.html", {"request": request, "error": str(e)})
