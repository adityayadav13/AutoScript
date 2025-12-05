import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
from dotenv import load_dotenv

# ================================
# LOAD ENVIRONMENT VARIABLES
# ================================
load_dotenv()  # Reads .env file locally

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing! Add it to .env or Render variables.")


# ================================
# FASTAPI APP
# ================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request format
class CompletionRequest(BaseModel):
    prefix: str
    language: str | None = None


# ================================
# COMPLETION ENDPOINT
# ================================

MODEL_NAME = "llama-3.3-70b-versatile"   # CURRENT NON-DEPRECATED MODEL


@app.post("/complete")
def complete_code(req: CompletionRequest):

    print("\n🔥 /complete called")
    print("Prefix:", req.prefix)

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are AutoScript — an inline AI code completion engine.\n"
                    "Continue the user's code from the exact cursor position.\n\n"
                    "RULES:\n"
                    "- NEVER repeat code already written.\n"
                    "- NEVER rewrite function headers.\n"
                    "- NEVER add comments or explanations.\n"
                    "- ONLY output what comes *next*.\n"
                    "- Maintain indentation and style.\n"
                ),
            },
            {
                "role": "user",
                "content": req.prefix,
            },
        ],
        "temperature": 0.1,
        "max_tokens": 120,
    }

    response = requests.post(url, headers=headers, json=payload)

    # If Groq responds with an error (quota, model, etc.)
    if response.status_code != 200:
        print("❌ GROQ ERROR:", response.text)
        return {"completion": ""}

    data = response.json()

    # Extract generated completion safely
    try:
        text = data["choices"][0]["message"]["content"]
    except Exception:
        text = ""

    print("➡️ AutoScript completion:", repr(text))

    return {"completion": text or ""}


# ================================
# ROOT ENDPOINT
# ================================

@app.get("/")
def home():
    return {"status": "AutoScript Backend Running ✔"}
