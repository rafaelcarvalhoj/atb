from repositories.llm import LlmRepository

class LlmService:
    def __init__(self, model: str, temperature: float = 0.7):
        self.__llm_repository = LlmRepository(temperature, model)
        
    def invoke(self, req):
        return self.__llm_repository.llm_client().invoke(req)