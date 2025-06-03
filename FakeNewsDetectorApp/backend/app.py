from flask import Flask, request, jsonify
from utils import fetch_fact_check, fetch_news_articles
from source_ranker import rank_sources
from llm_agent import generate_llm_reasoning

app = Flask(__name__)

@app.route("/check", methods=["POST"])
def check_news():
    data = request.get_json()
    query = data.get("query", "")
    
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    #Sources fetching
    fact_checks = fetch_fact_check(query)
    news_articles = fetch_news_articles(query)
    all_sources = fact_checks + news_articles

    #Rank
    ranked_sources = rank_sources(all_sources)

    #Analysis generation
    verdict = generate_llm_reasoning(query, ranked_sources)

    #Response retunr
    return jsonify({
        "query": query,
        "sources_used": ranked_sources,
        "llm_analysis": verdict
    })

if __name__ == "__main__":
    app.run(debug=True)
    port:5001
