def rank_sources(sources):
    ranked = []

    for s in sources:
        score = 0

        if "Google Fact Check" in s.get("source", ""):
            if "True" in s.get("verdict", ""):
                score += 10
            elif "False" in s.get("verdict", ""):
                score += 7
            else:
                score += 5

        if "News API" in s.get("source", "") or s.get("source") not in ["Google Fact Check", "Google Fact Check (via Gemini)"]:
            score += 3  # For just being a news result
            if "snippet" in s and s["snippet"]:
                score += 2
            if "title" in s and s["title"]:
                score += 2

        s["score"] = score
        ranked.append(s)

    return sorted(ranked, key=lambda x: x["score"], reverse=True)
