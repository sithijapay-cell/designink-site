import requests
from bs4 import BeautifulSoup
import json
import os
import re

def get_stats(keyword):
    url = f"https://stock.adobe.com/search?k={keyword.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results_text = soup.find(string=re.compile(r'results'))
        count = int(re.sub(r'[^\d]', '', results_text)) if results_text else 0
        
        # Score Logic: 100 - (count / divisor)
        score = max(5, min(99, int(100 - (count / 500))))
        return {"keyword": keyword, "supply": count, "score": score}
    except:
        return None

def main():
    with open("keywords.txt", "r") as f:
        keywords = list(set([line.strip() for line in f if line.strip()]))[-15:] # Keep last 15

    data = [get_stats(k) for k in keywords if get_stats(k)]
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()
