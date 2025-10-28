import asyncio
import requests
from summarizerbot.database import store_summary
from summarizerbot.nlp_logic import generate_research_summary
from summarizerbot.slack_notifier import send_to_slack

NEWS_API_KEY = "1bd6c59206644f809c7add3bae489280"
NEWS_URL = f"https://newsapi.org/v2/everything?q=artificial+intelligence&language=en&pageSize=5&apiKey={NEWS_API_KEY}"


async def fetch_latest_headlines():
    """Fetch latest AI or science-related articles."""
    try:
        response = requests.get(NEWS_URL)
        data = response.json()
        articles = []
        for item in data.get("articles", []):
            articles.append({
                "title": item["title"],
                "summary": item.get("description", ""),
                "link": item["url"]
            })
        return articles
    except Exception as e:
        print(f"⚠️ Failed to fetch news: {e}")
        return []


async def ambient_loop():
    """Continuously fetch and summarize new research/news every 5 minutes."""
    while True:
        try:
            print("\n🧠 Fetching new research/news updates...")
            # Ensure the coroutine runs properly
            articles = await asyncio.to_thread(lambda: asyncio.run(fetch_latest_headlines()))

            if not articles:
                print("⚠️ No new articles found.")
            else:
                for article in articles:
                    text_to_summarize = f"{article['title']}. {article['summary']}"
                    summary = generate_research_summary(text_to_summarize)

                    formatted = (
                        f"🧩 *New Summary Generated:*\n\n"
                        f"{summary}\n\n🔗 {article['link']}\n"
                    )

                    # 1️⃣ Save to database
                    store_summary(summary, article["link"])

                    # 2️⃣ Send to Slack
                    send_to_slack(formatted)

                    # 3️⃣ Print in console
                    print(formatted)

            print("✅ Sleeping for 5 minutes...\n")
        except Exception as e:
            print(f"[AmbientAgent Error] {e}")

        await asyncio.sleep(60)  # sleep for 5 minutes


def start_ambient_loop():
    """Entry point to start the background ambient loop."""
    loop = asyncio.get_event_loop()
    loop.create_task(ambient_loop())
    print("🌙 Ambient agent started (fetches every 5 minutes).")
