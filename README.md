# 🤖 AI Tech Watcher

AI 技术资讯聚合器 —— 自动抓取 AI 领域最新动态，通过大模型智能生成摘要和标签，推送到 iPhone 随时阅读。

## ✨ 功能特性

- 📡 **自动抓取**：定时从 OpenAI、Anthropic、Google AI、DeepMind 等官方博客获取最新文章
- 🧠 **AI 智能摘要**：调用 GPT-4o-mini 自动生成中文摘要、提取关键要点、评估重要度
- 📱 **移动端适配**：iOS 风格响应式界面，支持添加到主屏幕，体验接近原生 App
- 🗄️ **云端存储**：数据存入 Supabase，随时随地访问
- 🐳 **Docker 一键部署**：无需繁琐配置，一条命令上线

## 🛠️ 技术栈

| 类型 | 技术 |
|------|------|
| 后端 | Python 3.11 + Flask |
| 数据库 | Supabase (PostgreSQL) |
| AI | OpenAI API (GPT-4o-mini) |
| 部署 | Docker + Docker Compose |
| 前端 | 原生 HTML/CSS/JS，iOS 风格 UI |

## 📦 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/mester1103/ai-tech-watcher.git
cd ai-tech-watcher

### 2.配置环境变量
cp .env.example .env
nano .env

OPENAI_API_KEY=你的OpenAI_API_Key
SUPABASE_URL=你的Supabase_URL
SUPABASE_KEY=你的Supabase_Key

### 3. docker部署
docker-compose up -d --build

访问 http://你的服务器IP:5000 即可使用。
