"""
AI Content Generator using Google Gemini API
"""

import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

# ---------------- LOAD API KEY ----------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("❌ Please set GEMINI_API_KEY in your .env file!")

# ---------------- CONFIGURE GEMINI ----------------
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ---------------- ASYNC CONTENT GENERATION ----------------
async def generate_content(system_prompt, user_prompt):
    """Generate content using Gemini API"""
    spinner = ['|', '/', '-', '\\']
    done = False

    async def spin():
        idx = 0
        while not done:
            print(f"\r🤖 Generating content... {spinner[idx % len(spinner)]}", end='')
            idx += 1
            await asyncio.sleep(0.1)

    spinner_task = asyncio.create_task(spin())
    
    try:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        # Run blocking Gemini call in executor
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, model.generate_content, full_prompt)
        
        return response.text
    except Exception as e:
        raise Exception(f"Generation failed: {str(e)}")
    finally:
        done = True
        await spinner_task
        print("\r✅ Generation complete!               ")

# ---------------- CONTENT FUNCTIONS ----------------
async def generate_blog_post(prompt):
    system = "You are an expert blog writer. Write in a friendly, conversational style with headings and takeaways."
    return await generate_content(system, f"Write a complete blog post based on:\n{prompt}")

async def generate_twitter_posts(prompt):
    system = "You are a Twitter content expert. Write 5 engaging, punchy tweets max 280 characters with 2-3 hashtags."
    return await generate_content(system, f"Generate tweets based on:\n{prompt}")

async def generate_linkedin_posts(prompt):
    system = "You are a LinkedIn content strategist. Write 3-5 professional posts, 150-200 characters each, 1-2 hashtags."
    return await generate_content(system, f"Generate LinkedIn posts based on:\n{prompt}")

async def generate_instagram_caption(prompt):
    system = "You are an Instagram content creator. Write 3-5 engaging captions with hooks, emojis, hashtags, and CTA."
    return await generate_content(system, f"Generate Instagram captions based on:\n{prompt}")

async def generate_facebook_post(prompt):
    system = "You are a Facebook content specialist. Write 3-5 friendly, engaging posts with 1-2 hashtags."
    return await generate_content(system, f"Generate Facebook posts based on:\n{prompt}")

async def generate_email(prompt):
    system = "You are a professional email writer. Write a clear, concise email under 250 words with subject, greeting, body, CTA, and sign-off."
    return await generate_content(system, f"Write an email based on:\n{prompt}")

async def generate_product_description(prompt):
    system = "You are a copywriter. Write a compelling product description (150-200 words) focusing on benefits, pain points, and CTA."
    return await generate_content(system, f"Write a product description based on:\n{prompt}")

# ---------------- SAVE CONTENT ----------------
def save_content(content, content_type, prompt, index=None):
    if not os.path.exists("generated_content"):
        os.makedirs("generated_content")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_name = "_".join(prompt.split()[:5])
    short_name = "".join(c for c in short_name if c.isalnum() or c == "_")
    filename = f"generated_content/{content_type}_{short_name}"
    
    if index is not None:
        filename += f"_{index}"
    filename += f"_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Type: {content_type}\n")
        f.write(f"Request: {prompt}\n")
        f.write("="*70 + "\n\n")
        f.write(content)
    
    return filename

# ---------------- BATCH GENERATION ----------------
async def batch_generate(generator_func, prompts, content_type):
    tasks = [generator_func(p.strip()) for p in prompts]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, (p, r) in enumerate(zip(prompts, results), start=1):
        if isinstance(r, Exception):
            print(f"❌ Failed for prompt {i}: {r}")
            continue
        fname = save_content(r, content_type, p, i)
        print(f"💾 Saved content {i} to: {fname}")

# ---------------- MAIN PROGRAM ----------------
async def main():
    content_map = {
        "1": ("blog", generate_blog_post, "Blog"),
        "2": ("twitter", generate_twitter_posts, "Twitter"),
        "3": ("linkedin", generate_linkedin_posts, "LinkedIn"),
        "4": ("instagram", generate_instagram_caption, "Instagram"),
        "5": ("facebook", generate_facebook_post, "Facebook"),
        "6": ("email", generate_email, "Email"),
        "7": ("product", generate_product_description, "Product")
    }

    print("\n" + "="*70)
    print("🚀 AI CONTENT GENERATOR - GOOGLE GEMINI POWERED")
    print("="*70 + "\n")

    while True:
        print("\nSelect content type:")
        print("1. Blog Post")
        print("2. Twitter/X")
        print("3. LinkedIn")
        print("4. Instagram")
        print("5. Facebook")
        print("6. Email")
        print("7. Product Description")
        print("8. Exit")
        
        choice = input("\nChoose (1-8): ").strip()
        
        if choice == "8":
            print("\n👋 Exiting. Files saved in 'generated_content/'")
            break
        
        if choice not in content_map:
            print("❌ Invalid choice. Try again.")
            continue

        content_type, generator_func, content_name = content_map[choice]
        print(f"\n📝 {content_name} Generator")
        print("💡 Enter multiple prompts (one per line). Type 'END' to finish.\n")

        prompts = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            if line.strip():
                prompts.append(line.strip())

        if not prompts:
            print("❌ No prompts provided. Returning to menu.")
            continue

        await batch_generate(generator_func, prompts, content_type)

if __name__ == "__main__":
    asyncio.run(main())
