import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_FACT_CHECK_API_KEY = os.getenv("GOOGLE_FACT_CHECK_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

def fetch_fact_check(query):
    results = []
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GOOGLE_FACT_CHECK_API_KEY}"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": f"Fact-check this claim: {query}"}
                    ]
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if not response.content.strip():
            return [{"source": "Google Fact Check", "error": "Empty response from Gemini API"}]

        res = response.json()
        text = res.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        results.append({
            "source": "Google Fact Check (via Gemini)",
            "claim": query,
            "verdict": text.strip()
        })

    except Exception as e:
        results.append({"source": "Google Fact Check", "error": str(e)})

    return results


def fetch_news_articles(query):
    articles = []
    try:
        url = "https://serpapi.com/search.json"
        params = {
            "q": query,
            "tbm": "nws",
            "api_key": SERP_API_KEY
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for item in data.get("news_results", []):
            articles.append({
                "source": item.get("source", "Unknown"),
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "score": 0
            })

    except Exception as e:
        print(f"Error fetching news articles: {e}")
        articles.append({"source": "News API", "error": str(e)})

    return articles
