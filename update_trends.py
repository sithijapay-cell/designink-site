import os
import requests
import json
from groq import Groq

# Keys from GitHub Secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

client = Groq(api_key=GROQ_API_KEY)

def fetch_worldwide_market_data(keyword):
    # Fetch worldwide (geo="") historical interest
    url = f"https://serpapi.com/search.json?engine=google_trends&q={keyword}&geo=&api_key={SERPAPI_KEY}"
    try:
        res = requests.get(url).json()
        timeline = res.get('interest_over_time', {}).get('timeline_data', [])
        
        # Capture actual historical values for unique line graphs
        history = [day.get('values', [0])[0].get('value', 0) for day in timeline[-12:]]
        score = history[-1] if history else 0
        
        # Generate a Groq verdict based on the specific trend line
        trend_label = "rising" if history[-1] > history[0] else "stable"
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Keyword: {keyword}. Trend: {trend_label}. Give a realistic 10-word business advice for Adobe Stock contributors."}]
        )
        verdict = chat.choices[0].message.content

        return {
            "keyword": keyword,
            "score": score,
            "history": history, # True detail for the graph
            "verdict": verdict
        }
    except Exception as e:
        print(f"Error for {keyword}: {e}")
        return None

def main():
    if not os.path.exists("keywords.txt"):
        with open("keywords.txt", "w") as f: f.write("AI Landscapes\nNeon Portraits")

    with open("keywords.txt", "r") as f:
        keywords = [line.strip() for line in f if line.strip()][-10:]
    
    results = [fetch_worldwide_market_data(k) for k in keywords if fetch_worldwide_market_data(k)]
    
    # Save the data for the website
    with open("data.json", "w") as f:
        json.dump({
            "full_stream": results,
            "hot_list": sorted(results, key=lambda x: x['score'], reverse=True)[:5]
        }, f, indent=4)

if __name__ == "__main__":
    main()
