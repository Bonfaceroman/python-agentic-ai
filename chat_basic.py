

"""
My First AI Chat Program
Using Groq API
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY missing")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)




def chat(user_message):
    """Send a message to AI and get response"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Groq's fast model
        messages=[
            {
                "role": "system",
                "content": "You are a sentiment analyzer. classify text as positive, Negative, or Neutral."
            },
            {
                "role": "user",
                "content": " I love this product!"
            },
            {
                "role": "assistant",
                "content": "Sentiment: positive"
           },
            
           {
                "role": "user",
                "content": "This is terrible and broken"
           },
           {
               "role": "assistant",
               "content": "Sentiment: Negative"
           },
           {
              "role": "user",
              "content": "It's okay, nothing special"
           },
           {
             "role": "assistant",
             "content": "Sentiment: Neutral"
           },
           {
             "role": "user",
             "content":user_message
           }
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

def main():
    print("🤖 AI Chat with Groq Started!")
    print("Type 'quit' to exit\n")
    print("=" * 50 + "\n")
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Check if user wants to quit
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Goodbye! Thanks for chatting!")
            break
        
        # Skip empty messages
        if not user_input.strip():
            continue
        
        try:
            # Get AI response
            print("\n🤔 AI is thinking...\n")
            ai_response = chat(user_input)
            print(f"AI: {ai_response}\n")
            print("=" * 50 + "\n")
            
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            print("Make sure your API key is correct!\n")

if __name__ == "__main__":
    main()
