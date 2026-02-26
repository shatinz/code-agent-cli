import os
import sys
from dotenv import load_dotenv

# Load API keys BEFORE importing litellm/crewai so the environment is ready
load_dotenv()

from agents.team import create_team

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<your task description>\"")
        print("Example: python main.py \"Write a python script to fetch the weather in Tokyo\"")
        sys.exit(1)

    user_request = " ".join(sys.argv[1:])
    print(f"Starting Multiagent Orchestration Platform...")
    print(f"Task: {user_request}")
    print("-" * 50)

    try:
        crew = create_team(user_request)
        result = crew.kickoff()
        
        print("\n\n" + "=" * 50)
        print("TASK COMPLETE")
        print("=" * 50)
        print(result)
    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")

if __name__ == "__main__":
    main()
