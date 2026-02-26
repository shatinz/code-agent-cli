import os
import yaml
from litellm import completion

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

class LLMRouter:
    def __init__(self):
        self.config = load_config()
        self.primary_model = self.config["llm"]["primary"]["model"]
        self.fallback_models = [m["model"] for m in self.config["llm"]["fallbacks"]]

    def get_llm_config(self):
        """
        Since crewai uses LangChain LLMs under the hood (or litellm directly if configured),
        we provide the litellm model name. In the latest CrewAI, you can just pass the litellm model string.
        """
        return {
            "model": self.primary_model,
            "fallbacks": self.fallback_models
        }
    
    def chat_completion(self, messages, **kwargs):
        """
        Direct litellm completion if used outside CrewAI.
        """
        return completion(
            model=self.primary_model,
            messages=messages,
            fallbacks=self.fallback_models,
            **kwargs
        )

# For CrewAI, we typically initialize the LLM instances.
def get_crewai_llm():
    # CrewAI supports passing the litellm string format: "gemini/gemini-2.5-flash"
    router = LLMRouter()
    return router.primary_model
