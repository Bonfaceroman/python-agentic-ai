from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

response = client.chat.completions.create(
    model="groq/compound",
    messages=[{"role": "user", "content": "Write a short product description for noise-canceling headphones"}],
    temperature=0.8,
    max_tokens=200
)

print(response.choices[0].message.content)

