import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

# ===========================================
# CONFIG
# ===========================================

GROQ_API_KEY = "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"   # <-- PUT YOUR KEY HERE

# NEW WORKING MODEL (2025)
MODEL_NAME = "llama-3.3-70b-versatile"

if not GROQ_API_KEY:
    raise ValueError("❌ Missing GROQ API key")


# ===========================================
# FASTAPI APP
# ===========================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CompletionRequest(BaseModel):
    prefix: str
    language: str | None = None


# ===========================================
# COMPLETION ENDPOINT
# ===========================================

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
                    "You are AutoScript, a code completion engine.\n"
                    "Continue exactly where the user's code ends.\n\n"
                    "RULES:\n"
                    "- DO NOT repeat existing code.\n"
                    "- DO NOT rewrite functions or previous lines.\n"
                    "- Only output the next logical continuation.\n"
                    "- No comments, no explanations.\n"
                    "- Only raw code tokens."
                ),
            },
            {"role": "user", "content": req.prefix},
        ],
        "temperature": 0.1,
        "max_tokens": 120,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print("❌ GROQ ERROR:", response.text)
        return {"completion": ""}

    data = response.json()

    # Safe extraction
    try:
        text = data["choices"][0]["message"]["content"]
    except Exception:
        text = ""

    print("➡️ Returned completion:", repr(text))

    return {"completion": text or ""}


@app.get("/")
def root():
    return {"status": "AutoScript Backend OK"}
if __name__ == "__main__":
    import uvicorn
    print("⚡ AutoScript GROQ Backend running at http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)