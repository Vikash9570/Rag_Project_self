
from backend.app.services.generator import get_llm
from langchain_core.messages import SystemMessage, HumanMessage

def llm_test(message:str):
    response = get_llm().invoke('hi')
    print(response)


llm_test('hi')