# Example service using LangChain
from langchain.llms import Anthropic


class LLMService:
    def __init__(self, api_key: str):
        self.llm = Anthropic(api_key=api_key)

    def generate(self, prompt: str) -> str:
        return self.llm(prompt)
