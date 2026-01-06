import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("AIzaSyDXPD2RjYTWZU0OjhGPXA522Cvueux5FKs"))
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_niche():
    prompt = """
    Act as a Microstock Market Expert. Generate ONE specific, high-demand 
    keyword for Adobe Stock in 2026. Avoid generic terms. 
    Focus on niches like: Sustainable AI, Future of Work, or 2026 Gen-Z Aesthetics.
    Return ONLY the keyword text. Example: 'Solar-powered vertical drone delivery'
    """
    try:
        response = model.generate_content(prompt)
        new_keyword = response.text.strip()
        
        # Append to keywords.txt
        with open("keywords.txt", "a") as f:
            f.write(f"\n{new_keyword}")
        print(f"Added AI Niche: {new_keyword}")
    except Exception as e:
        print(f"AI Error: {e}")

if __name__ == "__main__":
    generate_niche()
