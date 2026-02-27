# Multiagent Orchestration Platform

Welcome to the **Multiagent Orchestration Platform**! This is a powerful, autonomous AI-powered assistant running natively on your local machine, now fully integrated with Telegram. Think of it as having an experienced senior software engineer right inside your messaging app, ready to take your complex goals and deliver working solutions automatically.

## ✨ What Can It Do?

Unlike standard conversational AI chat interfaces, this platform executes actions interactively on your system. It can autonomously command your terminal, write code, and search the web. 

1. **Cross-Platform Interactive Shell**: Ask the bot to run commands directly. It automatically detects if you're on Windows or Linux and uses Powershell or bash appropriately. Need to install dependencies, navigate directories, or check server status? Just ask.
2. **Token-Efficient Memory**: The bot is smart. If conversations run too long, it will silently summarize the history to conserve tokens, ensuring it never forgets the objective without breaking your API quota. Huge terminal outputs are safely truncated.
3. **Web Search**: It can query the web to download the latest documentation or gather external knowledge dynamically.
4. **Proxy Support**: Fully supports running the Telegram interface through a SOCKS5 proxy to bypass regional restrictions. 

The AI is powered by Gemini (defaulting to `gemini-2.5-pro` via LangChain).

---

## 🚀 Getting Started

### Prerequisites
- Make sure you have **Python 3.x** installed.
- Install the required packages via your terminal:
  ```bash
  pip install -r requirements.txt
  ```

### Configuration
1. **Set Up Keys and Tokens**: Open the provided `.env.example` file and save it as `.env`. Insert your API keys and tokens:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
   TELEGRAM_PROXY_URL="socks5://127.0.0.1:1080" # Optional: Leave blank if not needed
   ```

---

## 📱 How to Use It

Using the agent is simple and intuitive. Start the bot on your server/computer:

**Start the Platform:**
```bash
python main_telegram.py
```

**Chatting with the Bot:**
Open Telegram, find your bot, and send a message. You can speak to it naturally:
- *"What files are in the current directory?"*
- *"Run `npm run build` and tell me if there are errors."*
- *"Search the web for the latest Next.js documentation and summarize it."*

When you send a message, the agent reads your instructions, enters an autonomous execution loop (thinking, running shell commands, searching the web), and streams the final, verified solution right back to your chat.
