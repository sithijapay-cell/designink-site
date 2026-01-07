import os
from groq import Groq

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_niche():
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": "Generate ONE specific, high-demand keyword for Adobe Stock in 2026. Return ONLY the text. Example: 'Solar-powered vertical drone delivery'"
                }
            ],
        )
        new_keyword = completion.choices[0].message.content.strip()
        
        # Append to keywords.txt
        with open("keywords.txt", "a") as f:
            f.write(f"\n{new_keyword}")
        print(f"Added Groq Niche: {new_keyword}")
    except Exception as e:
        print(f"Groq Error: {e}")

if __name__ == "__main__":
    generate_niche()
