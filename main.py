# main.py

from agents.fetcher import fetch_articles
from agents.analyzer import analyze_all
from agents.reporter import generate_report


def main():
    print("=" * 50)
    print("   Intel AI News Agent")
    print("=" * 50)

    # Step 1: Fetch
    print("\n[Step 1] Fetching articles...")
    articles = fetch_articles()

    if not articles:
        print("[Main] No articles fetched. Check your RSS feeds or internet connection.")
        return

    # Step 2: Analyze
    print(f"\n[Step 2] Analyzing {len(articles)} articles for Intel relevance...")
    relevant_articles = analyze_all(articles)

    if not relevant_articles:
        print("[Main] No articles passed the relevance threshold. Try lowering RELEVANCE_THRESHOLD in config.py.")
        return

    # Step 3: Report
    print(f"\n[Step 3] Generating .docx report...")
    output_path = generate_report(relevant_articles)

    if output_path:
        print("\n" + "=" * 50)
        print(f"   Report ready: {output_path}")
        print("=" * 50)
    else:
        print("[Main] Report generation failed.")


if __name__ == "__main__":
    main()