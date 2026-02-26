import os
import json
from core.llm_router import LLMRouter
from tools.executor import execute_shell_command, execute_python_code
from tools.web_search import web_search
from tools.file_manager import read_file, write_file, list_directory

class NativeAgentTeam:
    def __init__(self):
        self.router = LLMRouter()
        self.tools_map = {
            "execute_shell_command": execute_shell_command,
            "execute_python_code": execute_python_code,
            "web_search": web_search,
            "read_file": read_file,
            "write_file": write_file,
            "list_directory": list_directory
        }
        
        # Litellm tools format
        self.litellm_tools = [
            {
                "type": "function",
                "function": {
                    "name": "execute_shell_command",
                    "description": "Executes a shell command directly on the host (Windows PowerShell).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "The shell command to execute"}
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_python_code",
                    "description": "Executes Python code safely by saving it to a temporary file and running it.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string", "description": "The full python script code to run"}
                        },
                        "required": ["code"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Searches the web using DuckDuckGo.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The search query"},
                            "max_results": {"type": "integer", "description": "Max number of results (default 5)"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Reads the contents of a file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Absolute or relative path to the file"}
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Writes or overwrites content to a file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Path to the file"},
                            "content": {"type": "string", "description": "The content to write"}
                        },
                        "required": ["file_path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "Lists the contents of a directory.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory_path": {"type": "string", "description": "Path to the directory, defaults to '.'"}
                        }
                    }
                }
            }
        ]

    def run(self, user_request: str) -> str:
        messages = [
            {"role": "system", "content": "You are a senior software engineer agent with full VPS access. "
                                          "You can search the web, execute shell commands, run python scripts, and manage files. "
                                          "Perform the user's request thoroughly. Once you have fully completed the task, "
                                          "explain what you did and why."},
            {"role": "user", "content": user_request}
        ]
        
        print("Agent thinking...")
        while True:
            response = self.router.chat_completion(
                messages=messages,
                tools=self.litellm_tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            messages.append(response_message)
            
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"\n[Tool Execution]: {function_name} with args: {function_args}")
                    
                    # For CrewAI we used the class's `run(...)` method if it was a subclass, 
                    # but here the tools were defined via `@tool` which actually makes them a class in CrewAI.
                    # Wait, our executor.py tools are still using `@tool` decorator from crewai!
                    # Let's handle both cases: if it has a .run() attribute, or if it's a direct function.
                    
                    tool = self.tools_map.get(function_name)
                    if tool:
                        try:
                            if hasattr(tool, 'run'):
                                result = tool.run(**function_args)
                            else:
                                result = tool(**function_args)
                            print(f"[Result]: \n{str(result)[:500]}...\n")
                        except Exception as e:
                            result = f"Error executing {function_name}: {str(e)}"
                            print(f"[Error]: {result}")
                    else:
                        result = f"Unknown tool: {function_name}"
                        
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": str(result)
                    })
            else:
                # No more tool calls, we are done
                return response_message.content

def create_team(user_request: str):
    # Backward compatibility for main.py expecting a wrapper with a kickoff method
    class TeamWrapper:
        def __init__(self, request):
            self.request = request
            self.team = NativeAgentTeam()
        def kickoff(self):
            return self.team.run(self.request)
            
    return TeamWrapper(user_request)
