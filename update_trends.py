import os
import requests
import json
from groq import Groq

# Keys from GitHub Secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

client = Groq(api_key=GROQ_API_KEY)

def fetch_worldwide_market_data(keyword):
    """Fetches real Google Trend history and a Groq AI expert opinion"""
    # Fetching worldwide (geo="") historical interest over 12 months
    url = f"https://serpapi.com/search.json?engine=google_trends&q={keyword}&geo=&api_key={SERPAPI_KEY}"
    
    try:
        response = requests.get(url)
        res = response.json()
        
        # Extract actual historical values for unique line graphs
        timeline = res.get('interest_over_time', {}).get('timeline_data', [])
        
        # We take the last 12 data points to show a clear trend on the site
        history = [day.get('values', [0])[0].get('value', 0) for day in timeline[-12:]]
        
        # If no data found, return None
        if not history:
            return None
            
        latest_score = history[-1]
        
        # Determine trend direction for a more realistic Groq verdict
        trend_label = "rising" if history[-1] > history[0] else "stable"
        
        # Get a real Groq opinion based on the actual trend direction
        prompt = f"The keyword '{keyword}' has a {trend_label} worldwide trend score of {latest_score}/100. Give a 10-word realistic business advice for an Adobe Stock contributor."
        
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        verdict = chat.choices[0].message.content

        return {
            "keyword": keyword,
            "score": latest_score,
            "history": history, # True detail for the unique line charts
            "verdict": verdict
        }
    except Exception as e:
        print(f"Error fetching data for {keyword}: {e}")
        return None

def main():
    # Ensure keywords file exists
    if not os.path.exists("keywords.txt"):
        with open("keywords.txt", "w") as f:
            f.write("AI Landscapes\nNeon Portraits\nCyberpunk Tech")

    # Read the last 10-15 keywords to analyze
    with open("keywords.txt", "r") as f:
        keywords = [line.strip() for line in f if line.strip()][-15:]
    
    # Process each keyword through SerpApi and Groq
    results = []
    for k in keywords:
        data = fetch_worldwide_market_data(k)
        if data:
            results.append(data)
    
    # Organize data for the website UI
    # 'full_stream' for the table, 'hot_list' for the sidebar
    final_data = {
        "full_stream": results,
        "hot_list": sorted(results, key=lambda x: x['score'], reverse=True)[:5]
    }
    
    # Save to data.json which the index.html reads
    with open("data.json", "w") as f:
        json.dump(final_data, f, indent=4)
    
    print(f"Successfully updated data.json with {len(results)} keywords.")

if __name__ == "__main__":
    main()
