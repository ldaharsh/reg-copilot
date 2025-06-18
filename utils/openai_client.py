# utils/openai_client.py
"""Thin wrapper around Azure OpenAI for fast reuse."""
import os, time
from typing import List, Dict
from dotenv import load_dotenv
import openai

load_dotenv()

_client = openai.AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

MODEL   = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

SYS_MSG = """
You are a senior regulatory scientist assisting biotech companies with USDA-CVB licensing applications. Reply clearly. Cite CFR sections when relevant. Keep tone concise.
Always format responses as **valid JSON**, using this schema:
{
  "summary": "string",
  "key_points": ["string", "string", ...],
  "cfr_citations": ["string", "string", ...]
}
Do **not** include any additional text or explanations outside JSON formatting.
Return ONLY structured JSON—no markdown, headers, or commentary.
"""

def chat(messages: List[Dict[str, str]],
         temperature: float = 0.4,
         stream: bool = False) -> openai.types.chat.ChatCompletion:
    """Send a list of messages (role/content) and return the completion."""
    start = time.time()
    response = _client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        stream=stream
    )
    duration = time.time() - start
    print(f"[openai] {response.usage.total_tokens} tokens • {duration:.1f}s")
    return response
