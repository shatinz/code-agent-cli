# AI Agent Technical Documentation

## Overview
Project: Multiagent Orchestration Platform (Custom Telegram-capable / CLI Agent)
Path: c:/Users/PC/prj/antigravity-telegram
Framework: LangChain & LangGraph with Python Telegram Bot
Language: Python 3.x

## System Architecture
The application runs as a LangGraph state machine. The primary interface is a Telegram bot that proxies user messages into the Graph. The graph consists of an LLM node (Gemini) that can choose to invoke tools, a Tool execution node, and a Summarizer node for memory management.

## Directory & File Structure
- `main_telegram.py`: The main entrypoint. Starts an asynchronous Telegram bot polling loop. Uses `python-telegram-bot` and supports SOCKS5 proxy routing via `httpx[socks]`. User messages are passed into the `agent_graph`.
- `requirements.txt`: Dependencies: `langchain`, `langgraph`, `langchain-google-genai`, `python-telegram-bot[socks]`, `httpx[socks]`, etc.
- `.env`: (Ignored in Git) Must contain `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, and optionally `TELEGRAM_PROXY_URL`.

### Core Module (`/core/`)
- `langchain_agent.py`: Defines the `AgentState` and constructs the LangGraph. 
  - **Memory & Token Efficiency:** Uses a conditional summarization node triggered when the chat history exceeds `MAX_MESSAGES`. Summarizes previous conversations into a concise string to save context tokens. It also handles truncating massive tool outputs.

### Tool Implementations (`/tools/`)
- `executor.py`: Sandbox bypass tools.
  - `InteractiveShellTool`: A custom LangChain Tool. Executes shell commands across platforms (Powershell on Windows, bash on Linux). Implements output truncation to prevent token overflow.
  - `execute_python_code(code: str)`: Executes inline python payloads dynamically.
- `file_manager.py`: Host filesystem abstractions for reading, writing, and listing files.
- `web_search.py`: `WebSearchTool` uses DuckDuckGo to return title, URL, and snippets.

## Execution Flow inside LangGraph
1. Execution starts via Telegram message in `main_telegram.py`, invoking `agent_graph.invoke()`.
2. Graph routes to `summarizer` node: Checks if `len(messages)` > limit. If so, synthesizes a summary of older messages to preserve token space and clears them from state.
3. Graph routes to `agent` node: Gemini processes the `SystemMessage` (containing instructions and current context summary) and user prompt.
4. If Gemini returns tool calls (`tools_condition`), graph routes to `tools` node. `InteractiveShellTool` or `WebSearchTool` execute natively.
5. Large outputs are defensively truncated inside the tools or summarizer before returning to the `agent` node.
6. Loop continues until Gemini outputs a plain text response without a tool call.
7. Graph finishes and returns the state to `main_telegram.py` which chunks and replies to the User over Telegram.
