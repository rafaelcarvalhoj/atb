import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class LlmRepository:
    def __init__(self, temperature: float, model: str):
        self.__temperature = temperature
        self.__model = model
    
    def llm_client(self) -> ChatGroq:
        return ChatGroq(
            temperature=self.__temperature,
            model=self.__model,
            api_key=os.environ.get("AI_API_KEY", "")
            )