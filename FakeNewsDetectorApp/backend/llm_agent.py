import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash-latest")

def generate_llm_reasoning(news_text, sources_summary):
    summary_text = ""
    for source in sources_summary[:5]:  # Limit to top 5 sources
        summary_text += f"\n- Source: {source.get('source')}\n  Snippet: {source.get('snippet', source.get('verdict', 'N/A'))}"

    prompt = f"""
You are a helpful AI fact-checker.

Claim: "{news_text}"

Sources:{summary_text if summary_text else "\n(No strong sources found)"}

Give a human-style explanation and then a final verdict as one of: "Likely True", "Likely False", or "Unclear".
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"
