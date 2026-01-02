import feedparser
import json
from datetime import datetime

# RSS feeds and sample category mapping
FEEDS = [
    {"url":"https://news.google.com/rss/search?q=Aerospace+Park+Bangalore", "category":"Others"},
    {"url":"https://news.google.com/rss/search?q=Aerospace+Park+Jobs", "category":"Jobs"},
    {"url":"https://news.google.com/rss/search?q=Aerospace+Park+Events", "category":"Events"},
    {"url":"https://news.google.com/rss/search?q=Aerospace+Park+Infra", "category":"Infra"}
]

try:
    with open("news.json","r") as f:
        existing = json.load(f)
except:
    existing = []

existing_links = {item["link"] for item in existing}

for feed in FEEDS:
    parsed = feedparser.parse(feed["url"])
    for entry in parsed.entries:
        if entry.link not in existing_links:
            existing.append({
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published",""),
                "category": feed["category"],
                "fetched_at": datetime.utcnow().isoformat()
            })

# Sort by date descending
existing.sort(key=lambda x: x.get("date",""), reverse=True)

with open("news.json","w") as f:
    json.dump(existing,f,indent=2)
