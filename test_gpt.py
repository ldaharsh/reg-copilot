import os
from dotenv import load_dotenv
import openai

load_dotenv()  # reads .env

client = openai.AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

response = client.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    messages=[{"role": "user",
               "content": "Tell me a short veterinarian joke."}]
)

msg = response.choices[0].message.content
usage = response.usage
print("GPT-4o says:", msg)
print("Tokens ➜ prompt", usage.prompt_tokens,
      "completion", usage.completion_tokens)
