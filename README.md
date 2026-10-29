# 🤖 AI 智能伴侣 (AI Companion)

一个基于 **Streamlit + DeepSeek / OpenAI 兼容接口** 的轻量级 AI 聊天伴侣 Web 应用。
用户可以在侧边栏自定义伴侣的**昵称**与**性格人设**，应用会以聊天的方式与你对话，并自动保存 / 加载 / 删除多轮会话记录。

> 本项目为个人学习作品，适合作为 Python / 全栈入门练手项目，也欢迎在此基础上二次开发。

---

## ✨ 功能特性

- 💬 **流式对话**：调用大模型接口，逐字流式输出，体验接近真人聊天
- 🎭 **可自定义人设**：通过侧边栏实时修改伴侣昵称与性格描述，对话风格随之变化
- 💾 **会话持久化**：自动将每一轮对话保存为本地 JSON，刷新 / 重启不丢失
- 📚 **历史会话管理**：侧边栏列出全部历史会话，支持一键**切换**与**删除**
- 🔐 **密钥安全**：API Key 通过环境变量（`.env`）注入，代码不硬编码任何密钥
- 🖼️ **简洁界面**：基于 Streamlit 快速搭建，无需前端知识即可拥有完整 Web UI

---

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 编程语言 | Python 3.9+ |
| Web 框架 | [Streamlit](https://streamlit.io/) |
| 大模型接口 | [OpenAI Python SDK](https://github.com/openai/openai-python)（兼容 DeepSeek 等 OpenAI 式 API） |
| 配置管理 | python-dotenv |
| 数据存储 | 本地 JSON 文件（`sessions/`） |

---

## 📁 目录结构

```
ai-companion/
├── app.py              # 主程序入口
├── resources/
│   └── img_1.png       # 应用 logo
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量模板（复制为 .env 后填写）
├── .gitignore          # 忽略规则（密钥 / 会话数据 / 缓存）
├── LICENSE             # MIT 许可证
└── README.md           # 项目说明
```

---

## 🚀 快速开始

### 1. 环境要求
- Python 3.9 及以上
- 一个 DeepSeek（或 OpenAI 兼容）API Key

### 2. 克隆并安装依赖
```bash
git clone https://github.com/<你的用户名>/ai-companion.git
cd ai-companion
pip install -r requirements.txt
```

### 3. 配置 API Key
复制环境变量模板并填入你的 Key：
```bash
cp .env.example .env
# 然后编辑 .env，将 your_api_key_here 替换为真实 Key
```
```ini
# .env
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 4. 运行
```bash
streamlit run app.py
```
浏览器会自动打开 `http://localhost:8501`，即可开始聊天。

---

## 📖 使用说明

1. 在左侧侧边栏的「伴侣信息」中填写**昵称**与**性格**，点击输入框开始对话；
2. 点击「新建会话」开始一轮全新对话；
3. 在「历史会话」中可切换回任意历史对话，或点击 💔 删除；
4. 所有会话自动保存在 `sessions/` 目录（已在 `.gitignore` 中忽略，不会提交到仓库）。

---

## 🔧 可扩展方向（面试加分项）

- 接入更多模型（OpenAI / 通义 / 文心 等）并通过 UI 切换
- 将会话数据改为数据库（SQLite / PostgreSQL）存储
- 增加用户登录与多用户隔离
- 部署到云服务器 / Streamlit Cloud，提供公开访问链接
- 增加对话导出、人设模板、语音输入等功能

---

## ⚠️ 免责声明

本应用中的「伴侣」为**虚构的角色扮演 AI**，所有回复均由大模型生成，仅供娱乐与学习交流，不代表任何真实个体或立场。请勿用于任何商业或误导性用途。

---

## 📄 许可证

本项目基于 [MIT License](./LICENSE) 开源。
