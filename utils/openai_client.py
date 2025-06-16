# utils/openai_client.py
"""
Thin wrapper around Azure OpenAI for fast reuse.
Handles token-usage printing only when the call is *not* streamed.
"""

import os
import time
from typing import List, Dict

from dotenv import load_dotenv
import openai

# ────────────────────────────────────────────────────────────────────────────────
# Environment & client setup
# ────────────────────────────────────────────────────────────────────────────────
load_dotenv()  # read .env once at import time

_client = openai.AzureOpenAI(
    api_key   = os.getenv("AZURE_OPENAI_KEY"),
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    base_url  = os.getenv("AZURE_OPENAI_ENDPOINT"),
)

MODEL   = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
SYS_MSG = (
    "You are a senior regulatory scientist helping biotech companies craft "
    "USDA-CVB submissions. Reply clearly, cite CFR sections when relevant, "
    "and keep tone concise."
)

# ────────────────────────────────────────────────────────────────────────────────
# Public helper
# ────────────────────────────────────────────────────────────────────────────────
def chat(
    messages: List[Dict[str, str]],
    temperature: float = 0.4,
    stream: bool = False,
):
    """
    Send a message list (role/content dictionaries) to GPT-4o.
    If `stream=True`, returns a Stream generator.
    For non-stream calls, prints token usage and returns the full response.
    """
    start = time.time()

    response = _client.chat.completions.create(
        model       = MODEL,
        messages    = messages,
        temperature = temperature,
        stream      = stream,
    )

    # `usage` exists only on non-stream responses (or final stream chunk)
    if not stream and hasattr(response, "usage"):
        duration = time.time() - start
        print(f"[openai] {response.usage.total_tokens} tokens • {duration:.1f}s")

    return response
