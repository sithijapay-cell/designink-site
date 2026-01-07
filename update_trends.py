import os
import requests
import json
import re
from groq import Groq

# Keys from GitHub Secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

client = Groq(api_key=GROQ_API_KEY)

def get_market_intelligence(keyword):
    # Fetch real Google Trend data via SerpApi
    url = f"https://serpapi.com/search.json?engine=google_trends&q={keyword}&api_key={SERPAPI_KEY}"
    try:
        res = requests.get(url).json()
        timeline = res.get('interest_over_time', {}).get('timeline_data', [])
        google_score = timeline[-1].get('values', [0])[0].get('value', 0) if timeline else 50
        
        # Get Groq Expert Opinion
        prompt = f"Keyword: {keyword}. Google Trend Score: {google_score}/100. Give a 10-word instruction for an Adobe Stock contributor."
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        opinion = chat.choices[0].message.content
        
        return {"keyword": keyword, "score": google_score, "opinion": opinion}
    except:
        return None

def main():
    # Load keywords and analyze
    with open("keywords.txt", "r") as f:
        keywords = [line.strip() for line in f if line.strip()][-10:]
    
    all_data = []
    for k in keywords:
        data = get_market_intelligence(k)
        if data: all_data.append(data)
    
    # Save top 5 for the Daily Hot List
    hot_list = sorted(all_data, key=lambda x: x['score'], reverse=True)[:5]
    
    final_output = {
        "full_stream": all_data,
        "hot_list": hot_list
    }
    
    with open("data.json", "w") as f:
        json.dump(final_output, f, indent=4)

if __name__ == "__main__":
    main()
