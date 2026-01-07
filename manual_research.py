import os
import requests
import json
from groq import Groq

# API Keys - Fetched from GitHub Secrets for security
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

client = Groq(api_key=GROQ_API_KEY)

def analyze_market_data(keyword):
    """Fetches real Google data and gets a Groq AI expert opinion"""
    print(f"--- Analyzing Market for: {keyword} ---")
    
    # 1. Fetch Real Google Search Trends via SerpApi
    search_url = f"https://serpapi.com/search.json?engine=google_trends&q={keyword}&api_key={SERPAPI_KEY}"
    
    try:
        response = requests.get(search_url)
        data = response.json()
        
        # Get the latest Interest Score (0-100) from the Google timeline
        timeline = data.get('interest_over_time', {}).get('timeline_data', [])
        google_score = timeline[-1].get('values', [0])[0].get('value', 0) if timeline else 50
        
        # 2. Consult Groq AI for a professional verdict
        prompt = (
            f"The keyword '{keyword}' has a Google Search interest of {google_score}/100. "
            f"As a Stock Market expert for Adobe Stock, give a 15-word verdict: "
            f"Should a contributor create content for this niche today?"
        )
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        
        opinion = completion.choices[0].message.content
        
        # Determine the user-friendly "Ease of Win" status
        status = "Very Easy" if google_score < 40 else ("Medium" if google_score < 75 else "High Competition")
        
        return {
            "keyword": keyword,
            "google_score": google_score,
            "opinion": opinion,
            "status": status,
            "profit_potential": "High Profit" if google_score > 60 else "Steady Sales"
        }
        
    except Exception as e:
        print(f"Research Error: {e}")
        return None

def main():
    # Example: Analyze a few core keywords to start the data.json file
    keywords = ["Eco Friendly AI", "Future Transport 2026", "Sustainable Interior"]
    results = []
    
    for k in keywords:
        res = analyze_market_data(k)
        if res:
            results.append(res)
    
    # Save the initial research results for the website UI
    with open("data.json", "w") as f:
        json.dump({"full_stream": results, "hot_list": results[:5]}, f, indent=4)
    print("Market research successfully updated in data.json")

if __name__ == "__main__":
    main()
