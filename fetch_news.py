import feedparser
import json
from datetime import datetime

# ---------- RSS Feeds ----------
FEEDS = [
    "https://news.google.com/rss/search?q=Aerospace+Park+Bangalore",
    "https://news.google.com/rss/search?q=KIADB+Aerospace+Park",
    "https://news.google.com/rss/search?q=Bangalore+Aerospace+SEZ",
]

# ---------- Keywords for category mapping ----------
CATEGORY_KEYWORDS = {
    "Jobs": ["job", "hiring", "recruitment", "vacancy", "career", "opening"],
    "Infra": ["road", "construction", "infrastructure", "building", "facility", "bridge", "park"],
    "Events": ["event", "celebration", "festival", "puja", "fair", "inauguration", "launch"],
    "Alerts": ["alert", "warning", "caution", "flood", "fire", "crime", "traffic", "maintenance"]
}

def guess_category(title: str) -> str:
    title_lower = title.lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in title_lower:
                return cat
    return "Others"

# ---------- Load existing news ----------
try:
    with open("news.json", "r") as f:
        existing = json.load(f)
except:
    existing = []

existing_links = {item["link"] for item in existing}

# ---------- Fetch news ----------
for feed_url in FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        if entry.link not in existing_links:
            category = guess_category(entry.title)
            existing.append({
                "title": entry.title,
                "link": entry.link,
                "date": entry.get("published",""),
                "category": category,
                "fetched_at": datetime.utcnow().isoformat()
            })
            existing_links.add(entry.link)

# ---------- Sort news by date descending ----------
def parse_date(d):
    try:
        return datetime.strptime(d, "%a, %d %b %Y %H:%M:%S %Z")
    except:
        return datetime.utcnow()

existing.sort(key=lambda x: parse_date(x.get("date","")), reverse=True)

# ---------- Save updated news ----------
with open("news.json", "w") as f:
    json.dump(existing, f, indent=2)
