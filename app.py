import os
import json
import subprocess
from flask import Flask, render_template_string, jsonify
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <title>AI 技术观察</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f2f2f7;
            padding: 16px;
            padding-top: 70px;
        }
        .header {
            position: fixed; top: 0; left: 0; right: 0;
            background: rgba(242,242,247,0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 12px 16px;
            border-bottom: 1px solid rgba(0,0,0,0.05);
            z-index: 100;
        }
        .header h1 { font-size: 32px; font-weight: 700; }
        .header-actions {
            position: absolute; right: 12px; top: 12px;
            display: flex; gap: 8px;
        }
        .btn {
            background: #007aff; color: white; border: none;
            padding: 6px 14px; border-radius: 20px;
            font-size: 13px; cursor: pointer;
        }
        .btn-fetch { background: #34c759; }
        .card {
            background: white;
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: transform 0.15s;
        }
        .card:active { transform: scale(0.99); background: #f8f8f8; }
        .source { color: #007aff; font-size: 13px; font-weight: 500; margin-bottom: 8px; }
        .title { font-size: 17px; font-weight: 600; margin-bottom: 6px; line-height: 1.3; }
        .one-liner { font-size: 14px; color: #8e8e93; margin-bottom: 10px; }
        .tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
        .tag {
            background: #f2f2f7;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            color: #636366;
        }
        .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
        }
        .stars { color: #ffcc00; font-size: 12px; }
        .time { color: #8e8e93; font-size: 12px; }
        .loading { text-align: center; padding: 40px; color: #8e8e93; }
        .toast {
            position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
            background: rgba(0,0,0,0.8); color: white; padding: 10px 20px;
            border-radius: 30px; font-size: 14px; z-index: 200;
            opacity: 0; transition: opacity 0.3s;
        }
        .toast.show { opacity: 1; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI 观察</h1>
        <div class="header-actions">
            <button class="btn" onclick="loadArticles()">刷新</button>
            <button class="btn btn-fetch" onclick="triggerFetch()">抓取</button>
        </div>
    </div>
    <div id="content" class="loading">加载中...</div>
    <div id="toast" class="toast"></div>

    <script>
        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        }

        async function loadArticles() {
            document.getElementById('content').innerHTML = '<div class="loading">加载中...</div>';
            try {
                const res = await fetch('/api/articles');
                const articles = await res.json();
                
                if (!articles.length) {
                    document.getElementById('content').innerHTML = '<div class="loading">暂无文章，点击「抓取」获取最新资讯</div>';
                    return;
                }
                
                let html = '';
                articles.forEach(a => {
                    const stars = '⭐'.repeat(a.importance || 3);
                    const tags = (a.tags || []).map(t => `<span class="tag">#${t}</span>`).join('');
                    const timeAgo = formatTime(a.published_at);
                    
                    html += `<div class="card" onclick="window.open('${a.url}', '_blank')">
                        <div class="source">📱 ${a.source_name}</div>
                        <div class="title">${a.title}</div>
                        <div class="one-liner">${a.one_liner || ''}</div>
                        <div class="tags">${tags}</div>
                        <div class="footer">
                            <span class="stars">${stars}</span>
                            <span class="time">${timeAgo}</span>
                        </div>
                    </div>`;
                });
                
                document.getElementById('content').innerHTML = html;
            } catch (e) {
                document.getElementById('content').innerHTML = '<div class="loading">加载失败，请重试</div>';
            }
        }

        async function triggerFetch() {
            showToast('🚀 开始抓取最新资讯...');
            try {
                const res = await fetch('/api/fetch', { method: 'POST' });
                const data = await res.json();
                showToast('✅ 抓取完成，刷新中...');
                loadArticles();
            } catch (e) {
                showToast('❌ 抓取失败');
            }
        }

        function formatTime(dateStr) {
            if (!dateStr) return '';
            const date = new Date(dateStr);
            const now = new Date();
            const diff = Math.floor((now - date) / 1000);
            if (diff < 60) return '刚刚';
            if (diff < 3600) return Math.floor(diff/60) + '分钟前';
            if (diff < 86400) return Math.floor(diff/3600) + '小时前';
            if (diff < 604800) return Math.floor(diff/86400) + '天前';
            return date.toLocaleDateString('zh-CN');
        }

        let touchStart = 0;
        document.addEventListener('touchstart', e => touchStart = e.touches[0].clientY);
        document.addEventListener('touchmove', e => {
            if (window.scrollY === 0 && e.touches[0].clientY - touchStart > 80) {
                loadArticles();
            }
        });

        loadArticles();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/articles')
def get_articles():
    try:
        res = supabase.table("ai_articles").select("*").order("published_at", desc=True).limit(50).execute()
        return jsonify(res.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fetch', methods=['POST'])
def trigger_fetch():
    try:
        subprocess.Popen(["python", "main.py"])
        return jsonify({"success": True, "message": "抓取任务已启动"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
