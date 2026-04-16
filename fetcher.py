import feedparser
from datetime import datetime
from typing import List, Dict

RSS_SOURCES = [
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml", "category": "官方博客"},
    {"name": "Anthropic News", "url": "https://www.anthropic.com/news/rss.xml", "category": "官方博客"},
    {"name": "Google AI Blog", "url": "https://blog.research.google/feeds/posts/default", "category": "研究进展"},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "category": "开源社区"},
    {"name": "Meta AI Blog", "url": "https://ai.meta.com/blog/rss/", "category": "研究进展"},
    {"name": "DeepMind Blog", "url": "https://deepmind.google/blog/rss.xml", "category": "研究进展"},
]

def fetch_articles() -> List[Dict]:
    articles = []
    for source in RSS_SOURCES:
        try:
            print(f"  正在抓取: {source['name']}...")
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:5]:
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])
                content = ""
                if hasattr(entry, 'content'):
                    content = entry.content[0].value
                elif hasattr(entry, 'summary'):
                    content = entry.summary
                elif hasattr(entry, 'description'):
                    content = entry.description
                article = {
                    "title": entry.title,
                    "url": entry.link,
                    "summary": entry.get("summary", ""),
                    "source_name": source["name"],
                    "source_category": source["category"],
                    "published_at": published.isoformat() if published else None,
                    "raw_content": content,
                }
                articles.append(article)
                print(f"    ✅ 获取: {entry.title[:40]}...")
        except Exception as e:
            print(f"    ❌ 抓取失败: {e}")
    return articles
