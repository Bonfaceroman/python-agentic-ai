# Memory Chatbot using Google Gemini (PaLM2) via Vertex AI

import os
from google.cloud import aiplatform

# ---------------- CONFIG ---------------- #
PROJECT_ID = "YOUR_PROJECT_ID"      # replace with your Google Cloud project ID
REGION = "us-central1"              # replace with your region

# If your venv has GOOGLE_APPLICATION_CREDENTIALS set, it will be used automatically
aiplatform.init(project=PROJECT_ID, location=REGION)

# Create a TextGenerationModel instance for chat
chat_model = aiplatform.TextGenerationModel.from_pretrained("chat-bison-001")

# ---------------- MEMORY BOT ---------------- #
class MemoryBot:
    def __init__(self, persona="helpful assistant"):
        self.history = [{"author": "system", "content": f"You are a {persona}."}]

    def chat(self, msg: str) -> str:
        self.history.append({"author": "user", "content": msg})

        # Combine all history as a single prompt
        conversation_text = ""
        for entry in self.history:
            role = "User" if entry["author"] == "user" else "AI"
            conversation_text += f"{role}: {entry['content']}\n"
        conversation_text += "AI: "

        try:
            response = chat_model.predict(
                conversation_text,
                temperature=0.7,
                max_output_tokens=400
            )
            reply = response.text
        except Exception as e:
            reply = f"[ERROR] API request failed: {e}"

        self.history.append({"author": "assistant", "content": reply})
        return reply

    def show_memory(self):
        print("\n" + "=" * 60)
        for msg in self.history[1:]:
            role = "YOU" if msg["author"] == "user" else "AI"
            print(f"{role}: {msg['content']}\n")
        print("=" * 60)

# ---------------- RUN CHATBOT ---------------- #
bot = MemoryBot("Python tutor who remembers student's progress")

print("🧠 MEMORY CHATBOT (Gemini) - I remember everything!\n")
print("Commands: 'memory' to see history, 'quit' to exit\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("quit", "exit"):
        print("\n👋 Goodbye!")
        break
    if user_input.lower() == "memory":
        bot.show_memory()
        continue

    reply = bot.chat(user_input)
    print(f"\nAI: {reply}\n")
