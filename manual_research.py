import google.generativeai as genai
import sys
import os

# Set your API Key
genai.configure(api_key="AIzaSyDXPD2RjYTWZU0OjhGPXA522Cvueux5FKs")
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_keyword(keyword):
    prompt = f"""
    Act as a professional Microstock Analyst. 
    Analyze the keyword: '{keyword}' for Adobe Stock in 2026.
    Provide a JSON response with:
    1. 'score': (A number 1-100 based on demand/supply gap)
    2. 'insight': (A 10-word professional tip)
    3. 'style': (Recommended visual style like 'Minimalist Vector' or 'Cinematic Photo')
    """
    response = model.generate_content(prompt)
    print(response.text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_keyword(sys.argv[1])
