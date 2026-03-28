import httpx
import json
import os
from dotenv import load_dotenv
from app.utils.prompt import build_prompt

load_dotenv(dotenv_path=".env")

HF_API_KEY = os.getenv("HF_API_KEY")

# Unified router endpoint (new HF standard)
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json",
}


async def fetch_word_data(word: str, book: str) -> dict:
    prompt = build_prompt(word, book)

    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",  # ✅ Free + deployed on Cerebras
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.7,
        "provider": "cerebras",   # ✅ Fast, free tier
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(HF_API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"HuggingFace API error: {response.status_code} - {response.text}")

    raw = response.json()
    generated_text = raw["choices"][0]["message"]["content"].strip()

    return parse_response(generated_text)


def parse_response(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse model response: {text}")