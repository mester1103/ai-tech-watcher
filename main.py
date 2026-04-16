import json
import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

from fetcher import fetch_articles
from ai_processor import batch_process_articles

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

def save_to_supabase(articles):
    saved = 0
    for article in articles:
        analysis = article.get("ai_analysis", {})
        data = {
            "title": article["title"],
            "url": article["url"],
            "source_name": article["source_name"],
            "source_category": article["source_category"],
            "published_at": article["published_at"],
            "key_points": json.dumps(analysis.get("key_points", [])),
            "tags": analysis.get("tags", []),
            "one_liner": analysis.get("one_liner", ""),
            "importance": analysis.get("importance", 3),
            "updated_at": datetime.now().isoformat()
        }
        try:
            supabase.table("ai_articles").upsert(data, on_conflict="url").execute()
            saved += 1
            print(f"  💾 已保存: {article['title'][:30]}...")
        except Exception as e:
            print(f"  ❌ 保存失败: {e}")
    return saved

def main():
    print(f"\n🚀 开始抓取...")
    articles = fetch_articles()
    print(f"📡 抓取 {len(articles)} 篇")
    
    processed = batch_process_articles(articles)
    print(f"🤖 分析保留 {len(processed)} 篇")
    
    saved = save_to_supabase(processed)
    print(f"💾 保存 {saved} 篇到数据库")

if __name__ == "__main__":
    main()
