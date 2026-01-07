import os
import requests
import json
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

client = Groq(api_key=GROQ_API_KEY)

def fetch_worldwide_trends(keyword):
    # Fetching worldwide (geo="") interest data from SerpApi
    url = f"https://serpapi.com/search.json?engine=google_trends&q={keyword}&geo=&api_key={SERPAPI_KEY}"
    try:
        res = requests.get(url).json()
        interest = res.get('interest_over_time', {}).get('timeline_data', [])
        
        # Get latest score and the Trend Graph Link from SerpApi
        latest_score = interest[-1].get('values', [0])[0].get('value', 0) if interest else 0
        
        # Use Groq for a short, data-only verdict
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Keyword: {keyword}. Trend: {latest_score}/100. Give a 5-word profit forecast."}]
        )
        verdict = chat.choices[0].message.content

        return {
            "keyword": keyword,
            "score": latest_score,
            "verdict": verdict,
            "region": "Worldwide"
        }
    except:
        return None

def main():
    if not os.path.exists("keywords.txt"):
        with open("keywords.txt", "w") as f: f.write("Minimalist AI Art\nCyberpunk 2026")

    with open("keywords.txt", "r") as f:
        keywords = [line.strip() for line in f if line.strip()][-10:]
    
    results = [fetch_worldwide_trends(k) for k in keywords if fetch_worldwide_trends(k)]
    
    # Save the top 5 for the Daily Hot List
    with open("data.json", "w") as f:
        json.dump({"full_stream": results, "hot_list": sorted(results, key=lambda x: x['score'], reverse=True)[:5]}, f, indent=4)

if __name__ == "__main__":
    main()
