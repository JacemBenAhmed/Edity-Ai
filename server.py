"""
FastAPI chat backend using OpenRouter API
Exposes:
  - POST /chat  → simple chat endpoint with system prompt
Requires .env:
  API_KEY=<your openrouter key>
  MODEL_NAME=tngtech/deepseek-r1t2-chimera:free
"""

import os
import json
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

load_dotenv()

app = FastAPI(title="AI Chat via OpenRouter")

SYSTEM_PROMPT = "You are a helpful AI assistant."


def call_openrouter(messages: list):
    url = "https://openrouter.ai/api/v1/chat/completions"

    API_KEY = os.getenv("API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME")

    if not API_KEY:
        raise HTTPException(500, "Missing API_KEY in .env")

    if not MODEL_NAME:
        raise HTTPException(500, "Missing MODEL_NAME in .env")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost", 
        "X-Title": "local-chat",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        raise HTTPException(response.status_code, response.text)

    return response.json()


@app.post("/chat")
def chat(payload: dict):
    user_prompt = payload.get("prompt")
    if not user_prompt:
        raise HTTPException(400, "Missing prompt")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    result = call_openrouter(messages)

    content = result["choices"][0]["message"]["content"]

    return JSONResponse({"response": content})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
