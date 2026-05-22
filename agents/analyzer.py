# agents/analyzer.py

import cohere
import config
import time

client = cohere.ClientV2(api_key=config.COHERE_API_KEY)

def analyze_article(article):
    prompt = f"""You are an Intel industry analyst. Evaluate this news article strictly for its relevance to Intel Corporation.

Article Title: {article['title']}
Article Snippet: {article['summary']}

Your tasks:
1. Give a relevance score from 1 to 10.
   - 9-10: Directly about Intel (products, strategy, financials, partnerships)
   - 7-8: Significantly affects Intel (competitor moves, market shifts, AI trends Intel is part of)
   - 4-6: Loosely related (general semiconductor or AI industry news)
   - 1-3: Not relevant to Intel

2. Write WHY this matters to Intel in 2 sentences. Be specific to Intel, not generic.

3. Write a 3 sentence summary of the article.

Respond ONLY in this exact format, no extra text:
SCORE: <number>
WHY_IT_MATTERS: <2 sentences>
SUMMARY: <3 sentences>"""

    try:
        response = client.chat(
            model="command-a-03-2025",
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.message.content[0].text.strip()
        score   = None
        why     = ""
        summary = ""

        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("SCORE:"):
                try:
                    score = int(line.replace("SCORE:", "").strip())
                except ValueError:
                    pass
            elif line.startswith("WHY_IT_MATTERS:"):
                why = line.replace("WHY_IT_MATTERS:", "").strip()
            elif line.startswith("SUMMARY:"):
                summary = line.replace("SUMMARY:", "").strip()

        if score is None or score < config.RELEVANCE_THRESHOLD:
            print(f"[Analyzer] DROPPED (score {score}): {article['title'][:60]}")
            return None

        print(f"[Analyzer] KEPT (score {score}): {article['title'][:60]}")

        return {
            "title":           article["title"],
            "link":            article["link"],
            "source":          article["source"],
            "relevance_score": score,
            "why_it_matters":  why,
            "summary":         summary
        }

    except Exception as e:
        print(f"[Analyzer] ERROR: {article['title'][:60]} — {e}")
        return None


def analyze_all(articles):
    results = []

    for i, article in enumerate(articles):
        print(f"[Analyzer] Processing {i+1}/{len(articles)}...")
        result = analyze_article(article)
        if result:
            results.append(result)
        time.sleep(2)

    print(f"[Analyzer] {len(results)} articles passed relevance threshold.")
    return results