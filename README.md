# AI Agent Technical Documentation

## Overview
Project: Multiagent Orchestration Platform (Custom Telegram-capable / CLI Agent)
Path: c:/Users/PC/prj/antigravity-telegram
Framework: Custom event loop built on `litellm` (Direct API bridging) avoiding bloated abstractions, with local system access.
Language: Python 3.x

## System Architecture
The application runs a synchronous loop that proxies OpenAI-compatible tool calls mapped to native Python functions. The LLM handles logic and tool sequencing autonomously until completion. Configured via `config.yaml` but dynamically orchestrated in `agents/team.py`.

## Directory & File Structure
- `main.py`: CLI entrypoint. Takes user request as trailing arguments. Initializes `create_team(user_request).kickoff()`.
- `config.yaml`: Contains configuration. Noteworthy sections:
  - `llm`: primary model (e.g., `gemini/gemini-2.5-flash`) and fallbacks (`gemini-2.5-pro` etc).
  - `agents`: Defines PM, Engineer, Reviewer personas (mostly structural, currently the codebase relies heavily on the Engineer persona).
- `requirements.txt`: Minimal dependencies: `litellm`, `duckduckgo-search`, `pydantic`, `python-dotenv`, `google-generativeai`.
- `.env`: (Ignored in Git) Must contain API keys (e.g. `GEMINI_API_KEY`) for litellm to consume.

### Core Module (`/core/`)
- `llm_router.py`: `LLMRouter` class reads `config.yaml` to parse `primary` and `fallbacks`. Exposes `chat_completion()` wrapping `litellm.completion` to manage model routing logic automatically.

### Agent Loop (`/agents/`)
- `team.py`: `NativeAgentTeam` and `create_team(user_request)`. 
  - `NativeAgentTeam.__init__`: Defines `self.litellm_tools` array schemas (execute_shell_command, execute_python_code, web_search, read_file, write_file, list_directory) and `self.tools_map` pointing to actual Python tool functions.
  - `NativeAgentTeam.run(user_request)`: Core iterative LLM tool-calling loop. Bootstraps with a System Prompt enforcing a "senior software engineer" persona with full VPS access. Parses tool calls from Litellm response, executes mapped python function directly, injecting the serialized result back as `{"role": "tool", "content": result_str}`. Returns final text when no more tools are requested.

### Tool Implementations (`/tools/`)
- `executor.py`: Sandbox bypass tools.
  - `execute_shell_command(command: str)`: Runs via synchronous subprocess in `powershell`. Timeout 120s. Captures STDOUT/STDERR.
  - `execute_python_code(code: str)`: Executes inline python payloads by writing to a temporary file, invoking `python`, capturing output, and auto-deleting the payload file. Timeout 120s.
- `file_manager.py`: Host filesystem abstractions.
  - `read_file(file_path: str)`: utf-8 read.
  - `write_file(file_path: str, content: str)`: Creates path directories if missing, utf-8 overwrite.
  - `list_directory(directory_path: str = ".")`: Returns `os.listdir` string serialization.
- `web_search.py`: Knowledge acquisition.
  - `web_search(query: str, max_results: int = 5)`: Uses DuckDuckGo (`DDGS().text`) to return search results formatted as Title, URL, and Snippet.

## Execution Flow for Agent Readers
1. Execution starts at `main.py` -> `create_team()` -> `NativeAgentTeam.run()`.
2. Initial messages array generated including `{"role": "system", ...}` and `{"role": "user", ...}`.
3. Enters `while True:` tool-calling loop.
4. `router.chat_completion` receives tools array.
5. If `response_message.tool_calls` exist, iterate -> `json.loads(arguments)` -> dynamic invocation from `self.tools_map` -> append output to `messages`.
6. Break loop and `return response_message.content` when LLM ceases tool requests.
