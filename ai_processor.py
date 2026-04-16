import os
import json
from dotenv import load_dotenv
from typing import List, Dict, Optional
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.longcat.chat/openai/v1"
)

SYSTEM_PROMPT = """你是一个专业的AI技术新闻编辑。你的任务是：
1. 判断文章是否与AI技术相关（如果不相关，标记为过滤）
2. 提取核心技术要点（3个）
3. 打上合适的标签
4. 用一句话总结这篇文章的核心价值
5. 评估重要程度（1-5分）

请严格按照以下JSON格式回复：
{
    "is_relevant": true/false,
    "key_points": ["要点1", "要点2", "要点3"],
    "tags": ["标签1", "标签2"],
    "one_liner": "一句话总结",
    "importance": 1-5
}"""

def process_article(article: Dict) -> Optional[Dict]:
    user_message = f"""
标题：{article['title']}
来源：{article['source_name']}
原文摘要：{article['summary'][:500]}
正文片段：{article['raw_content'][:1000]}

请分析这篇文章是否与AI技术相关，并提取关键信息。
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        if result.get("is_relevant", False):
            article["ai_analysis"] = result
            return article
        else:
            print(f"    🔄 过滤无关文章")
            return None
    except Exception as e:
        print(f"    ❌ AI处理失败: {e}")
        return None

def batch_process_articles(articles: List[Dict]) -> List[Dict]:
    processed = []
    for i, article in enumerate(articles, 1):
        print(f"  [{i}/{len(articles)}] 处理: {article['title'][:30]}...")
        result = process_article(article)
        if result:
            processed.append(result)
    return processed
